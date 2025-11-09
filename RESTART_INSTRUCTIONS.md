# MCP Server Restart Instructions

## Problem
Claude Desktop is running an OLD version of the pdf-to-csv server from before we fixed the pdfplumber API compatibility issue.

## Solution
**You MUST restart Claude Desktop** for it to load the updated server code.

## Steps to Restart Claude Desktop

### Option 1: Complete Restart (Recommended)
1. **Quit Claude Desktop completely**
   - Click "Claude" in the menu bar
   - Click "Quit Claude" (or press Cmd+Q)

2. **Wait 2-3 seconds**

3. **Reopen Claude Desktop**

### Option 2: Force Restart MCP Servers
If you don't want to quit Claude Desktop completely, you can try:
1. Open a new conversation in Claude Desktop
2. The servers should reload automatically

## How to Verify It's Working

After restarting, ask Claude Desktop:

```
Use pdf-to-csv to extract tables from sample_PDF.pdf
```

If it works, you should see:
- ✓ PDF: sample_PDF.pdf
- ✓ Pages: 1
- ✓ Tables found: 1
- ✓ CSV files created

If you still see the error `TableSettings.__init__() got an unexpected keyword argument 'strategy'`, then Claude Desktop didn't reload the server properly.

## What We Fixed

The old code used:
```python
ts = dict(strategy="lines", ...)  # ❌ Wrong - not supported by pdfplumber
```

The new code uses:
```python
ts = {
    "vertical_strategy": "lines",    # ✓ Correct
    "horizontal_strategy": "lines",  # ✓ Correct
    ...
}
```

## Current Server Status

✅ File has been updated with the correct API calls
✅ Local testing works perfectly
❌ Claude Desktop is running the old cached version
🔄 **ACTION NEEDED: Restart Claude Desktop**
