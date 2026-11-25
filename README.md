# PDF to CSV MCP Server

[![CI](https://github.com/sergiudanstan/mcp-pdf-to-csv/actions/workflows/ci.yml/badge.svg)](https://github.com/sergiudanstan/mcp-pdf-to-csv/actions/workflows/ci.yml)
[![CodeQL](https://github.com/sergiudanstan/mcp-pdf-to-csv/actions/workflows/codeql.yml/badge.svg)](https://github.com/sergiudanstan/mcp-pdf-to-csv/actions/workflows/codeql.yml)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/sergiudanstan/mcp-pdf-to-csv/badge)](https://scorecard.dev/viewer/?uri=github.com/sergiudanstan/mcp-pdf-to-csv)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

FastMCP server for extracting tables from PDF files and converting them to CSV format.

## Features

- **Batch PDF processing**: Extract tables from single or multiple PDFs
- **Multiple extraction strategies**: Auto, lattice (grid-based), and stream (whitespace-based)
- **Flexible output**: Save individual tables or merge all tables per PDF
- **Configurable folders**: Set custom input/output directories

> **Security:** the tools are not confined to the configured folders; they can read PDFs from, and write CSVs to, any path your user can access. See [SECURITY.md](SECURITY.md).

## Installation

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

The server is configured in Claude Desktop at:
`~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "pdf-to-csv": {
      "command": "/path/to/mcp-pdf-to-csv/.venv/bin/python3",
      "args": ["/path/to/mcp-pdf-to-csv/pdf_to_csv_server.py"]
    }
  }
}
```

## Usage

### Default Folders
- **Input**: `pdfs/` next to `pdf_to_csv_server.py`
- **Output**: `output_csv/` next to `pdf_to_csv_server.py`

### Available MCP Tools

1. **set_folder(folder: str)**
   - Set the input folder containing PDF files
   - Example: `set_folder("/path/to/pdfs")`

2. **set_output(folder: str)**
   - Set the output folder for CSV files
   - Example: `set_output("/path/to/output")`

3. **list_pdfs()**
   - List all PDF files in the current input folder

4. **extract_tables(filename: str, pages: str = "all", strategy: str = "auto", merge: bool = False, strip_ws: bool = True)**
   - Extract tables from a single PDF
   - **Parameters**:
     - `filename`: PDF filename in the input folder
     - `pages`: "all" or specific pages like "1,3-5"
     - `strategy`: "auto", "lattice", or "stream"
     - `merge`: Create merged CSV with all tables
     - `strip_ws`: Strip whitespace from cells

5. **extract_all(pages: str = "all", strategy: str = "auto", merge: bool = False, strip_ws: bool = True)**
   - Extract tables from all PDFs in the folder
   - Same parameters as extract_tables (except filename)

6. **show_config()**
   - Display current input/output folder configuration

## Testing

```bash
pip install -r requirements.txt pytest
python -m pytest -q tests
```

The tests generate small PDFs with ruled tables, extract them with the real `pdfplumber`, and call the tools through an in-memory MCP client.

## Troubleshooting

### Check Claude Desktop Logs
```bash
tail -50 ~/Library/Logs/Claude/mcp-server-pdf-to-csv.log
```

### Common Issues

1. **"Read-only file system" error**: Fixed by using absolute paths (SCRIPT_DIR)
2. **Connection errors**: Restart Claude Desktop after configuration changes
3. **Missing dependencies**: Reinstall with `pip install -r requirements.txt`

## Technical Details

- **Framework**: FastMCP 2.13.0.2
- **PDF Library**: pdfplumber (with pdfminer.six backend)
- **Data Processing**: pandas
- **Transport**: STDIO (Standard Input/Output)
- **Protocol**: MCP (Model Context Protocol) 2025-06-18

## Files

- `pdf_to_csv_server.py` - Main MCP server
- `tests/` - Test suite
- `README.md` - This file
- `.venv/` - Python virtual environment
- `pdfs/` - Default input folder
- `output_csv/` - Default output folder

## Development

```bash
pip install -r requirements.txt pytest
python -m pytest -q tests     # the tests generate their own PDFs
```

See [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md) (the tools can read and write anywhere your user can; read the threat model) and [CHANGELOG.md](CHANGELOG.md). The current version is in [VERSION](VERSION).
