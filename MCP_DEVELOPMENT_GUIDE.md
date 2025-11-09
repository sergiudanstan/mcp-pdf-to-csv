# Complete Guide: Building an MCP Server from Scratch

A step-by-step tutorial for creating a Model Context Protocol (MCP) server that integrates with Claude Desktop.

---

## Part 1: Understanding MCP

### What is MCP?
- **MCP (Model Context Protocol)** is a protocol that allows Claude to interact with external tools and data sources
- It enables you to create custom servers that Claude can call to perform specific tasks
- MCP servers expose "tools" that Claude can use during conversations

### Key Concepts
- **Server**: A Python program that runs and listens for tool calls
- **Tools**: Functions that Claude can invoke (like `extract_tables`, `list_pdfs`, etc.)
- **Transport**: How Claude communicates with your server (usually STDIO - standard input/output)
- **Client**: Claude Desktop acts as the MCP client

---

## Part 2: Initial Setup

### Step 1: Create Project Directory
```bash
# Create a new folder for your MCP server
mkdir my_mcp_server
cd my_mcp_server
```

### Step 2: Set Up Python Virtual Environment
```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate  # On macOS/Linux
# OR
.venv\Scripts\activate     # On Windows
```

### Step 3: Install FastMCP
```bash
# FastMCP is the easiest way to create MCP servers
pip install fastmcp

# Install any additional libraries you need
# For example, for PDF processing:
pip install pdfplumber pandas
```

---

## Part 3: Writing Your MCP Server

### Step 4: Create Your Server File

Create a file called `server.py`:

```python
from fastmcp import FastMCP

# Create the MCP server instance
mcp = FastMCP("my-server-name")

# Define your first tool
@mcp.tool()
def hello_world(name: str) -> str:
    """Say hello to someone."""
    return f"Hello, {name}!"

# Run the server
if __name__ == "__main__":
    mcp.run()
```

### Step 5: Understanding Tool Decorators

**Basic Tool Structure:**
```python
@mcp.tool()
def tool_name(parameter1: type, parameter2: type = default) -> return_type:
    """
    Tool description - this appears in Claude Desktop.

    Explain what the tool does and how to use it.
    """
    # Your code here
    return result
```

**Key Points:**
- Use type hints (`: str`, `: int`, `: bool`, etc.)
- Add docstrings - Claude uses these to understand what the tool does
- Return values should be strings or simple types
- Optional parameters should have default values

### Step 6: Add State Management (If Needed)

For servers that need to track state:

```python
from pathlib import Path
from dataclasses import dataclass

# Get the script's directory
SCRIPT_DIR = Path(__file__).parent.absolute()

@dataclass
class Settings:
    input_folder: Path = SCRIPT_DIR / "input"
    output_folder: Path = SCRIPT_DIR / "output"

settings = Settings()

# Create directories
try:
    settings.input_folder.mkdir(parents=True, exist_ok=True)
    settings.output_folder.mkdir(parents=True, exist_ok=True)
except (OSError, PermissionError):
    pass  # Handle gracefully
```

**Important:** Always use **absolute paths**, not relative paths!

### Step 7: Add Multiple Tools

```python
@mcp.tool()
def set_input_folder(folder: str) -> str:
    """Set the input folder path."""
    p = Path(folder).expanduser()
    p.mkdir(parents=True, exist_ok=True)
    settings.input_folder = p
    return f"Input folder set to: {p}"

@mcp.tool()
def list_files() -> str:
    """List all files in the input folder."""
    files = [f.name for f in settings.input_folder.iterdir() if f.is_file()]
    if not files:
        return "No files found."
    return "\n".join(files)

@mcp.tool()
def process_file(filename: str, option: str = "default") -> str:
    """
    Process a file with the given option.

    Args:
        filename: Name of the file to process
        option: Processing option (default, advanced, etc.)
    """
    file_path = settings.input_folder / filename

    if not file_path.exists():
        return f"Error: File not found: {filename}"

    # Your processing logic here
    result = f"Processed {filename} with option: {option}"
    return result
```

---

## Part 4: Testing Your Server

### Step 8: Test Locally

Create a test script `test_server.py`:

```python
#!/usr/bin/env python3
"""Test the MCP server"""

import sys
sys.path.insert(0, '.')

from server import mcp, settings

def test_server():
    print("Testing MCP Server")
    print("=" * 50)

    print(f"\nSettings:")
    print(f"  Input folder: {settings.input_folder}")
    print(f"  Output folder: {settings.output_folder}")

    print(f"\nRegistered Tools:")
    # List your expected tools
    expected_tools = ["set_input_folder", "list_files", "process_file"]
    for tool in expected_tools:
        print(f"  - {tool}")

    print("\n✓ Server configuration is valid!")

if __name__ == "__main__":
    test_server()
```

Run the test:
```bash
python test_server.py
```

### Step 9: Test MCP Protocol

Test that the server responds to MCP messages:

```bash
# Send an initialization message
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' | python server.py
```

You should see a JSON response with server capabilities.

---

## Part 5: Integrating with Claude Desktop

### Step 10: Find Claude Desktop Config

The configuration file is located at:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

### Step 11: Add Your Server to Config

Edit `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "my-server-name": {
      "command": "/absolute/path/to/my_mcp_server/.venv/bin/python3",
      "args": ["/absolute/path/to/my_mcp_server/server.py"]
    }
  }
}
```

**Critical Points:**
- Use **absolute paths** only (e.g., `/Users/yourname/...`)
- Don't use `~` or `./` - expand to full paths
- The `command` should point to your virtual environment's Python
- The `args` should point to your server script

**Example:**
```json
{
  "mcpServers": {
    "pdf-processor": {
      "command": "/Users/sara/my_mcp_server/.venv/bin/python3",
      "args": ["/Users/sara/my_mcp_server/server.py"]
    }
  }
}
```

### Step 12: Validate JSON Config

```bash
# Check if your JSON is valid
python3 -m json.tool < ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

If there are syntax errors, fix them before proceeding.

### Step 13: Restart Claude Desktop

**Complete restart required:**
1. Quit Claude Desktop completely (Cmd+Q on Mac, or File → Quit)
2. Wait 3-5 seconds
3. Reopen Claude Desktop

---

## Part 6: Testing in Claude Desktop

### Step 14: Verify Server Connection

In Claude Desktop, ask:
```
What MCP servers are currently connected?
```

Or:
```
Show me the tools available from my-server-name
```

### Step 15: Test Your Tools

Try calling your tools:
```
Use my-server-name to list files
```

```
Use the process_file tool from my-server-name to process example.txt
```

### Step 16: Check Logs for Errors

If something doesn't work, check the logs:

**macOS:**
```bash
tail -50 ~/Library/Logs/Claude/mcp-server-my-server-name.log
```

**Windows:**
```powershell
Get-Content "$env:APPDATA\Claude\logs\mcp-server-my-server-name.log" -Tail 50
```

---

## Part 7: Common Issues and Solutions

### Issue 1: "Read-only file system" Error

**Problem:** Using relative paths like `./input`

**Solution:** Use absolute paths
```python
# ❌ Bad
folder = Path("./input")

# ✓ Good
SCRIPT_DIR = Path(__file__).parent.absolute()
folder = SCRIPT_DIR / "input"
```

### Issue 2: Server Disconnects Immediately

**Problem:** Error during initialization (in global scope)

**Solution:** Wrap initialization in try-except
```python
try:
    settings.folder.mkdir(parents=True, exist_ok=True)
except (OSError, PermissionError):
    pass  # Will create later when needed
```

### Issue 3: Changes Not Reflected

**Problem:** Claude Desktop caches the old server code

**Solution:** Always restart Claude Desktop after code changes

### Issue 4: Library API Changes

**Problem:** External library parameters changed

**Solution:** Check library documentation and update parameters
```python
# Old API (might not work)
result = library.process(strategy="auto")

# New API (check docs)
result = library.process(
    vertical_strategy="auto",
    horizontal_strategy="auto"
)
```

### Issue 5: Tool Not Showing Up

**Checklist:**
- [ ] Did you use `@mcp.tool()` decorator?
- [ ] Is the function defined before `mcp.run()`?
- [ ] Did you restart Claude Desktop?
- [ ] Check the logs for errors

---

## Part 8: Best Practices

### Code Organization

```python
# 1. Imports
from fastmcp import FastMCP
from pathlib import Path
from dataclasses import dataclass
import your_libraries

# 2. Constants
SUPPORTED_FORMATS = {".pdf", ".txt"}
SCRIPT_DIR = Path(__file__).parent.absolute()

# 3. Settings/State
@dataclass
class Settings:
    folder: Path = SCRIPT_DIR / "data"

settings = Settings()

# 4. Helper Functions (not exposed to MCP)
def _internal_helper(data):
    """Helper function - not an MCP tool."""
    return processed_data

# 5. MCP Server Instance
mcp = FastMCP("server-name")

# 6. MCP Tools
@mcp.tool()
def public_tool(param: str) -> str:
    """Tool that Claude can call."""
    return _internal_helper(param)

# 7. Main Entry Point
if __name__ == "__main__":
    print(f"Starting server...")
    print(f"Data folder: {settings.folder}")
    mcp.run()
```

### Error Handling

```python
@mcp.tool()
def safe_tool(filename: str) -> str:
    """Tool with proper error handling."""
    try:
        # Your logic here
        result = process_file(filename)
        return f"Success: {result}"
    except FileNotFoundError:
        return f"Error: File not found: {filename}"
    except PermissionError:
        return f"Error: Permission denied accessing {filename}"
    except Exception as e:
        return f"Error: {str(e)}"
```

### Documentation

```python
@mcp.tool()
def well_documented_tool(
    input_file: str,
    output_format: str = "csv",
    include_headers: bool = True
) -> str:
    """
    Convert a file to the specified format.

    This tool processes the input file and converts it to the desired
    output format. Supports multiple formats and options.

    Args:
        input_file: Path to the input file (relative to input folder)
        output_format: Output format (csv, json, xml). Default: csv
        include_headers: Include column headers in output. Default: True

    Returns:
        Success message with output file path, or error message

    Example:
        convert_file("data.txt", "csv", True)
    """
    # Implementation
    pass
```

---

## Part 9: Complete Example

Here's the complete PDF to CSV server as a reference:

```python
"""
PDF to CSV Converter MCP Server
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Any
from pathlib import Path

import pdfplumber
import pandas as pd
from fastmcp import FastMCP

# Constants
SUPPORTED_EXT = {".pdf"}
SCRIPT_DIR = Path(__file__).parent.absolute()

# Settings
@dataclass
class Settings:
    folder: Path = SCRIPT_DIR / "pdfs"
    output_dir: Path = SCRIPT_DIR / "output_csv"

settings = Settings()

# Safe initialization
try:
    settings.folder.mkdir(parents=True, exist_ok=True)
    settings.output_dir.mkdir(parents=True, exist_ok=True)
except (OSError, PermissionError):
    pass

# Helper function
def list_pdfs_in_folder(folder: Path) -> List[str]:
    if not folder.is_dir():
        return []
    return sorted([
        p.name for p in folder.iterdir()
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXT
    ])

# MCP Server
mcp = FastMCP("pdf-to-csv")

@mcp.tool()
def set_folder(folder: str) -> str:
    """Set the input folder containing PDF files."""
    p = Path(folder).expanduser()
    p.mkdir(parents=True, exist_ok=True)
    settings.folder = p
    return f"Folder set to: {p}\nPDFs found: {len(list_pdfs_in_folder(p))}"

@mcp.tool()
def list_pdfs() -> str:
    """List available PDF filenames in the current folder."""
    pdfs = list_pdfs_in_folder(settings.folder)
    if not pdfs:
        return "No PDFs found."
    return "\n".join(pdfs)

@mcp.tool()
def show_config() -> str:
    """Show current configuration (input folder, output folder)."""
    return f"folder={settings.folder}\noutput_dir={settings.output_dir}"

# Main entry point
if __name__ == "__main__":
    print(f"Starting PDF to CSV MCP...")
    print(f"- folder: {settings.folder}")
    print(f"- output: {settings.output_dir}")
    mcp.run()
```

---

## Part 10: Deployment Checklist

Before considering your MCP server "production ready":

- [ ] All tools have clear docstrings
- [ ] Error handling in all tools
- [ ] Use absolute paths throughout
- [ ] Test locally with test script
- [ ] Test MCP protocol communication
- [ ] Add to Claude Desktop config
- [ ] Restart Claude Desktop
- [ ] Test each tool in Claude Desktop
- [ ] Check logs for errors
- [ ] Create README with usage instructions
- [ ] Document any special setup requirements

---

## Quick Reference

### File Structure
```
my_mcp_server/
├── .venv/                 # Virtual environment
├── server.py              # Main MCP server
├── test_server.py         # Test script
├── README.md              # Documentation
├── input/                 # Input data folder
└── output/                # Output data folder
```

### Essential Commands
```bash
# Setup
python3 -m venv .venv
source .venv/bin/activate
pip install fastmcp

# Test
python test_server.py

# Run manually
python server.py

# Check logs
tail -f ~/Library/Logs/Claude/mcp-server-name.log
```

### Config Template
```json
{
  "mcpServers": {
    "server-name": {
      "command": "/absolute/path/to/.venv/bin/python3",
      "args": ["/absolute/path/to/server.py"]
    }
  }
}
```

---

## Resources

- **FastMCP Docs**: https://gofastmcp.com
- **MCP Protocol**: https://modelcontextprotocol.io
- **Debugging Guide**: https://modelcontextprotocol.io/docs/tools/debugging
- **Example Servers**: https://github.com/modelcontextprotocol/servers

---

## Summary

Building an MCP server involves:

1. **Setup** - Create project, virtual environment, install FastMCP
2. **Code** - Write server with `@mcp.tool()` decorated functions
3. **Test** - Test locally and verify MCP protocol
4. **Configure** - Add to Claude Desktop config with absolute paths
5. **Deploy** - Restart Claude Desktop and test in production
6. **Debug** - Check logs if issues arise
7. **Iterate** - Update code, restart Claude Desktop, repeat

**Remember:** Always use absolute paths, always restart Claude Desktop after changes, and always check the logs when debugging!
