"""Tests for pdf_to_csv_server: real PDFs are generated in the test, parsed by pdfplumber,
and the CSV files the tools write are checked."""

import asyncio
import csv
from pathlib import Path

import pytest
from fastmcp import Client

import pdf_to_csv_server as server


def make_table_pdf(path: Path, rows: list[list[str]], pages: int = 1) -> None:
    """Write a minimal PDF whose pages each contain a ruled table (lines + text)."""
    cw, rh, x0, y0 = 120, 30, 50, 700
    ncol = len(rows[0])
    stream = []
    for r in range(len(rows) + 1):
        y = y0 - r * rh
        stream.append(f"{x0} {y} m {x0 + ncol * cw} {y} l S")
    for c in range(ncol + 1):
        x = x0 + c * cw
        stream.append(f"{x} {y0} m {x} {y0 - len(rows) * rh} l S")
    for r, row in enumerate(rows):
        for c, text in enumerate(row):
            stream.append(f"BT /F1 12 Tf {x0 + c * cw + 6} {y0 - r * rh - 20} Td ({text}) Tj ET")
    content = "\n".join(stream).encode()

    objs = [b"<< /Type /Catalog /Pages 2 0 R >>"]
    kids = " ".join(f"{3 + 2 * i} 0 R" for i in range(pages))
    objs.append(f"<< /Type /Pages /Kids [{kids}] /Count {pages} >>".encode())
    font_id = 3 + 2 * pages
    for i in range(pages):
        objs.append(
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents {4 + 2 * i} 0 R "
            f"/Resources << /Font << /F1 {font_id} 0 R >> >> >>".encode()
        )
        objs.append(b"<< /Length %d >>\nstream\n" % len(content) + content + b"\nendstream")
    objs.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for n, body in enumerate(objs, start=1):
        offsets.append(len(out))
        out += b"%d 0 obj\n" % n + body + b"\nendobj\n"
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
    for off in offsets:
        out += b"%010d 00000 n \n" % off
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, xref)
    path.write_bytes(bytes(out))


ROWS = [["Item", "Qty", "Price"], ["Bolt", "10", "0.25"], ["Nut", "20", "0.10"]]


@pytest.fixture()
def dirs(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    inp, out = tmp_path / "in", tmp_path / "out"
    inp.mkdir()
    out.mkdir()
    monkeypatch.setattr(server.settings, "folder", inp)
    monkeypatch.setattr(server.settings, "output_dir", out)
    return inp, out


def read_csv(path: str) -> list[list[str]]:
    with open(path, newline="") as f:
        return list(csv.reader(f))


class TestExtraction:
    def test_lattice_table_roundtrip(self, dirs) -> None:
        inp, out = dirs
        make_table_pdf(inp / "inv.pdf", ROWS)
        res = server.extract_pdf_tables(inp / "inv.pdf", strategy="lattice")
        assert res["page_count"] == 1 and res["tables_found"] == 1
        assert read_csv(res["csv_files"][0]) == ROWS
        assert Path(res["csv_files"][0]).parent == out

    def test_merge_concatenates_tables_from_all_pages(self, dirs) -> None:
        inp, _ = dirs
        make_table_pdf(inp / "two.pdf", ROWS, pages=2)
        res = server.extract_pdf_tables(inp / "two.pdf", strategy="lattice", merge=True)
        assert res["tables_found"] == 2 and len(res["csv_files"]) == 2
        assert read_csv(res["merged_csv"]) == ROWS + ROWS

    def test_page_selection(self, dirs) -> None:
        inp, _ = dirs
        make_table_pdf(inp / "two.pdf", ROWS, pages=2)
        res = server.extract_pdf_tables(inp / "two.pdf", pages_spec="2", strategy="lattice")
        assert res["tables_found"] == 1 and res["csv_files"][0].endswith("two__p2_t1.csv")

    def test_missing_pdf_raises(self, dirs) -> None:
        inp, _ = dirs
        with pytest.raises(FileNotFoundError):
            server.extract_pdf_tables(inp / "nope.pdf")

    def test_list_pdfs_only_lists_pdfs(self, dirs) -> None:
        inp, _ = dirs
        make_table_pdf(inp / "b.pdf", ROWS)
        make_table_pdf(inp / "a.PDF", ROWS)
        (inp / "notes.txt").write_text("x")
        assert server.list_pdfs_in_folder(inp) == ["a.PDF", "b.pdf"]


class TestMcpTools:
    def test_tools_are_registered_and_callable_over_mcp(self, dirs) -> None:
        inp, out = dirs
        make_table_pdf(inp / "inv.pdf", ROWS)

        async def run():
            async with Client(server.mcp) as client:
                names = {t.name for t in await client.list_tools()}
                listed = await client.call_tool("list_pdfs", {})
                extracted = await client.call_tool("extract_tables", {"filename": "inv.pdf", "strategy": "lattice"})
                return names, listed.content[0].text, extracted.content[0].text

        names, listed, extracted = asyncio.run(run())
        assert names == {"set_folder", "set_output", "list_pdfs", "extract_tables", "extract_all", "show_config"}
        assert listed == "inv.pdf"
        assert "tables=1" in extracted and any(out.glob("inv__p1_t1.csv"))

    def test_extract_tables_reports_errors_as_text(self, dirs) -> None:
        async def run():
            async with Client(server.mcp) as client:
                return (await client.call_tool("extract_tables", {"filename": "missing.pdf"})).content[0].text

        assert asyncio.run(run()).startswith("Error:")
