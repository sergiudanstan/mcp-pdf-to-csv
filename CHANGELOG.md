# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project uses
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.1] - 2026-11-26

### Fixed
- The startup banner was printed to stdout, the JSON-RPC channel of the stdio transport, and
  could break the client's handshake. It now goes to stderr; a test starts the server over
  stdio and checks that stdout carries only JSON-RPC messages.

### Changed
- Removed the root-level notes that only described how the repository was created and pushed
  (`GITHUB_*.md`, `PUSH_STEPS.md`, `DEPLOYMENT_SUMMARY.md`, `DEPLOYMENT_COMPARISON.md`,
  `INDEX.md`, `RESTART_INSTRUCTIONS.md`). The quick start, remote deployment and MCP
  development guides moved to `docs/`, with personal paths replaced by placeholders.
- README: the framework line now matches `requirements.txt` (`fastmcp>=4.2.4`).
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
