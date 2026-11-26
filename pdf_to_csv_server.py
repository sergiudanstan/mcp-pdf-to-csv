"""
PDF to CSV Converter MCP Server (FastMCP)
Author: Dan's assistant

Features
- Folder-based batch PDF table extraction using pdfplumber
- Tools to set input/output folders, list PDFs, extract from one/all PDFs
- Supports strategies: "auto", "lattice" (grid-like), "stream" (whitespace-based)
- Saves CSVs per page/table; optional merged CSV per PDF

Quick start
-----------
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\\Scripts\\activate
pip install fastmcp pdfplumber pandas
python pdf_to_csv_server.py

MCP tools
---------
- set_folder(folder: str)
- set_output(folder: str)
- list_pdfs()
- extract_tables(filename: str, pages: str = "all", strategy: str = "auto", merge: bool = False, strip_ws: bool = True)
- extract_all(pages: str = "all", strategy: str = "auto", merge: bool = False, strip_ws: bool = True)
- show_config()
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Dict, Any

import sys
from pathlib import Path

import pdfplumber
import pandas as pd
from fastmcp import FastMCP

SUPPORTED_EXT = {".pdf"}

# ----------------- Global Config / State -----------------

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent.absolute()

@dataclass
class Settings:
    folder: Path = SCRIPT_DIR / "pdfs"
    output_dir: Path = SCRIPT_DIR / "output_csv"

settings = Settings()

# Create directories only if they don't exist and we have write permissions
try:
    settings.folder.mkdir(parents=True, exist_ok=True)
    settings.output_dir.mkdir(parents=True, exist_ok=True)
except (OSError, PermissionError) as e:
    # If we can't create dirs at startup, that's OK - we'll create them when needed
    pass

# ----------------- Utility / Core -----------------

def list_pdfs_in_folder(folder: Path) -> List[str]:
    if not folder.is_dir():
        return []
    return sorted([p.name for p in folder.iterdir() if p.is_file() and p.suffix.lower() in SUPPORTED_EXT])

def _extract_tables_from_page(page, strategy: str, strip_ws: bool):
    import pandas as pd
    dfs: List[pd.DataFrame] = []

    def _extract(strategy_name: str):
        # Use the correct parameter names for pdfplumber TableSettings
        if strategy_name == "lines":
            # Lines-based detection (lattice)
            ts = {
                "vertical_strategy": "lines",
                "horizontal_strategy": "lines",
                "snap_tolerance": 3,
                "intersection_tolerance": 3
            }
        else:
            # Text-based detection (stream)
            ts = {
                "vertical_strategy": "text",
                "horizontal_strategy": "text",
                "snap_tolerance": 3,
                "intersection_tolerance": 3
            }
        tables = page.extract_tables(table_settings=ts) or []
        frames = []
        for tbl in tables:
            maxlen = max((len(r) for r in tbl), default=0)
            norm = [ ([(c or "").strip() if strip_ws and isinstance(c, str) else (c or "") for c in (r + [""]*(maxlen-len(r)))]) for r in tbl ]
            df = pd.DataFrame(norm)
            frames.append(df)
        return frames

    if strategy == "auto":
        frames = _extract("lines")
        if not frames:
            frames = _extract("text")
        dfs.extend(frames)
    elif strategy == "lattice":
        dfs.extend(_extract("lines"))
    else:
        dfs.extend(_extract("text"))
    return dfs

def extract_pdf_tables(
    pdf_path: Path,
    pages_spec: str = "all",
    strategy: str = "auto",
    merge: bool = False,
    strip_ws: bool = True,
) -> Dict[str, Any]:
    results = {
        "filename": pdf_path.name,
        "page_count": 0,
        "tables_found": 0,
        "csv_files": [],
        "merged_csv": None,
    }
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    # Ensure output directory exists
    settings.output_dir.mkdir(parents=True, exist_ok=True)

    all_frames: List[pd.DataFrame] = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        results["page_count"] = len(pdf.pages)
        if pages_spec == "all":
            indices = range(len(pdf.pages))
        else:
            parts = [p.strip() for p in pages_spec.split(",") if p.strip()]
            idxs = set()
            for part in parts:
                if "-" in part:
                    a, b = part.split("-", 1)
                    a, b = int(a), int(b)
                    for k in range(a, b + 1):
                        idxs.add(k - 1)
                else:
                    idxs.add(int(part) - 1)
            indices = sorted([i for i in idxs if 0 <= i < len(pdf.pages)])

        table_idx = 0
        for pi in indices:
            page = pdf.pages[pi]
            dfs = _extract_tables_from_page(page, strategy=strategy, strip_ws=strip_ws)
            if not dfs:
                continue
            for j, df in enumerate(dfs, start=1):
                table_idx += 1
                out_name = f"{pdf_path.stem}__p{pi+1}_t{j}.csv"
                out_path = settings.output_dir / out_name
                df.to_csv(out_path, index=False, header=False)
                results["csv_files"].append(str(out_path))
                all_frames.append(df)
        results["tables_found"] = table_idx

    if merge and all_frames:
        merged = pd.concat(all_frames, ignore_index=True)
        merged_name = f"{pdf_path.stem}__merged.csv"
        merged_path = settings.output_dir / merged_name
        merged.to_csv(merged_path, index=False, header=False)
        results["merged_csv"] = str(merged_path)

    return results

def extract_all_pdfs(
    pages: str = "all",
    strategy: str = "auto",
    merge: bool = False,
    strip_ws: bool = True,
) -> str:
    pdfs = list_pdfs_in_folder(settings.folder)
    if not pdfs:
        return "No PDFs found."
    lines = []
    for fn in pdfs:
        try:
            res = extract_pdf_tables(
                settings.folder / fn,
                pages_spec=pages,
                strategy=strategy,
                merge=merge,
                strip_ws=strip_ws,
            )
            lines.append(f"{res['filename']}: pages={res['page_count']} tables={res['tables_found']} CSVs={len(res['csv_files'])}" + (f" merged={res['merged_csv']}" if res['merged_csv'] else ""))
        except Exception as e:
            lines.append(f"{fn}: ERROR: {e}")
    return "\n".join(lines)

# ----------------- FastMCP Server -----------------

mcp = FastMCP("pdf-to-csv")

@mcp.tool()
def set_folder(folder: str) -> str:
    """Set the input folder containing PDF files."""
    p = Path(folder).expanduser()
    p.mkdir(parents=True, exist_ok=True)
    settings.folder = p
    return f"Folder set to: {p}\nPDFs found: {len(list_pdfs_in_folder(p))}"

@mcp.tool()
def set_output(folder: str) -> str:
    """Set the output folder where CSV files will be written."""
    p = Path(folder).expanduser()
    p.mkdir(parents=True, exist_ok=True)
    settings.output_dir = p
    return f"Output set to: {p}"

@mcp.tool()
def list_pdfs() -> str:
    """List available PDF filenames in the current folder."""
    pdfs = list_pdfs_in_folder(settings.folder)
    if not pdfs:
        return "No PDFs found."
    return "\n".join(pdfs)

@mcp.tool()
def extract_tables(
    filename: str,
    pages: str = "all",
    strategy: str = "auto",
    merge: bool = False,
    strip_ws: bool = True,
) -> str:
    """
    Extract tables from a single PDF.
    - pages: "all" or like "1,3-5"
    - strategy: "auto", "lattice", "stream"
    - merge: write a merged CSV that concatenates all tables
    - strip_ws: strip whitespace from cells
    """
    try:
        res = extract_pdf_tables(
            settings.folder / filename,
            pages_spec=pages,
            strategy=strategy,
            merge=merge,
            strip_ws=strip_ws,
        )
        lines = [
            f"{res['filename']} -> pages={res['page_count']} tables={res['tables_found']}"
        ]
        for p in res["csv_files"]:
            lines.append(f"CSV: {p}")
        if res["merged_csv"]:
            lines.append(f"MERGED: {res['merged_csv']}")
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def extract_all(
    pages: str = "all",
    strategy: str = "auto",
    merge: bool = False,
    strip_ws: bool = True,
) -> str:
    """Extract tables from all PDFs in the folder."""
    return extract_all_pdfs(pages=pages, strategy=strategy, merge=merge, strip_ws=strip_ws)

@mcp.tool()
def show_config() -> str:
    """Show current configuration (input folder, output folder)."""
    return f"folder={settings.folder}\noutput_dir={settings.output_dir}"

if __name__ == "__main__":
    print("Starting PDF to CSV MCP (FastMCP) ...", file=sys.stderr)
    print(f"- folder: {settings.folder}", file=sys.stderr)
    print(f"- output: {settings.output_dir}", file=sys.stderr)
    mcp.run()
