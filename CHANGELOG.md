# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project uses
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Python 3.11 is now the minimum (3.10 reached end of life in October 2026). CI tests 3.11 and
  3.13. `pandas` floor raised to 3.1.1, which needs Python 3.11+.

## [0.1.0] - 2026-11-25

`mcp-pdf-to-csv` is a FastMCP server (one file, `pdf_to_csv_server.py`, stdio) that extracts
tables from PDF files with `pdfplumber` and writes them as CSV: six tools to set the input and
output folders, list PDFs, extract tables from one or all PDFs (auto, lattice or stream
strategy, page selection, optional merged CSV) and show the configuration.

### Added
- Test suite (`tests/`): PDFs with ruled tables are generated in the test and extracted with the
  real `pdfplumber`; covers CSV contents, merge, page selection, error handling, and the tools
  called through an in-memory MCP client.
- CI (tests on Python 3.10 and 3.13, ruff, `pip-audit`, `zizmor`), CodeQL, OpenSSF Scorecard
  and a tag-triggered release workflow with CycloneDX SBOM and build provenance; Dependabot for
  actions and pip.
- `SECURITY.md` (documents that the folder and file arguments are not confined),
  `CONTRIBUTING.md`, this changelog and a `VERSION` file as the single version source.

### Changed
- README: install and test instructions now match the repository (`requirements.txt`, `tests/`;
  the referenced `test_server.py` did not exist), machine-specific example paths replaced with
  placeholders, security note added.
- `.gitignore`: `tests/test_*.py` is no longer ignored by the `test_*.py` rule.

[Unreleased]: https://github.com/sergiudanstan/mcp-pdf-to-csv/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/sergiudanstan/mcp-pdf-to-csv/releases/tag/v0.1.0
