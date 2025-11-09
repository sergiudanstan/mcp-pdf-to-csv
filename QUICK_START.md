# MCP Server Quick Start Guide

## 5-Minute Setup

### 1. Create Project
```bash
mkdir my_mcp && cd my_mcp
python3 -m venv .venv
source .venv/bin/activate
pip install fastmcp
```

### 2. Create `server.py`
```python
from fastmcp import FastMCP
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.absolute()
mcp = FastMCP("my-server")

@mcp.tool()
def hello(name: str) -> str:
    """Say hello to someone."""
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()
```

### 3. Test It
```bash
python server.py &
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' | python server.py
```

### 4. Add to Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "/FULL/PATH/TO/my_mcp/.venv/bin/python3",
      "args": ["/FULL/PATH/TO/my_mcp/server.py"]
    }
  }
}
```

**Replace `/FULL/PATH/TO/` with your actual path!**

### 5. Restart Claude Desktop
- Quit completely (Cmd+Q)
- Reopen
- Ask: "Use my-server to say hello to World"

---

## Common Patterns

### State Management
```python
from dataclasses import dataclass

@dataclass
class Settings:
    folder: Path = SCRIPT_DIR / "data"

settings = Settings()
settings.folder.mkdir(parents=True, exist_ok=True)
```

### Multiple Tools
```python
@mcp.tool()
def set_folder(path: str) -> str:
    """Change the working folder."""
    settings.folder = Path(path)
    return f"Set to: {settings.folder}"

@mcp.tool()
def list_files() -> str:
    """List files in folder."""
    files = [f.name for f in settings.folder.iterdir()]
    return "\n".join(files)
```

### Error Handling
```python
@mcp.tool()
def process(filename: str) -> str:
    """Process a file."""
    try:
        # Your code
        return "Success"
    except FileNotFoundError:
        return f"Error: {filename} not found"
    except Exception as e:
        return f"Error: {e}"
```

---

## Debugging Checklist

Problem? Check these in order:

1. **Server won't start**
   - [ ] Check logs: `tail ~/Library/Logs/Claude/mcp-server-NAME.log`
   - [ ] Run manually: `python server.py`
   - [ ] Check for syntax errors

2. **Tools not appearing**
   - [ ] Restarted Claude Desktop?
   - [ ] Used `@mcp.tool()` decorator?
   - [ ] Check config JSON is valid

3. **Path errors**
   - [ ] Using absolute paths? Not `./` or `~`
   - [ ] Paths exist?
   - [ ] Permissions correct?

4. **Changes not working**
   - [ ] Saved the file?
   - [ ] Restarted Claude Desktop?
   - [ ] Check file modification time vs server start time

---

## Golden Rules

1. ✅ **Always use absolute paths**
   ```python
   # Good
   SCRIPT_DIR = Path(__file__).parent.absolute()
   folder = SCRIPT_DIR / "data"

   # Bad
   folder = Path("./data")
   ```

2. ✅ **Always restart Claude Desktop after code changes**

3. ✅ **Always wrap initialization in try-except**
   ```python
   try:
       folder.mkdir(parents=True, exist_ok=True)
   except (OSError, PermissionError):
       pass
   ```

4. ✅ **Always add docstrings to tools**
   ```python
   @mcp.tool()
   def my_tool(param: str) -> str:
       """This description appears in Claude Desktop."""
       return result
   ```

5. ✅ **Always check logs when debugging**

---

## Need More Help?

- Full guide: `MCP_DEVELOPMENT_GUIDE.md`
- FastMCP docs: https://gofastmcp.com
- MCP spec: https://modelcontextprotocol.io
