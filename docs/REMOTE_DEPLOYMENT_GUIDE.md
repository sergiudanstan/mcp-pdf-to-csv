# Deploying MCP Server Remotely and Connecting to Claude

This guide covers deploying your MCP server to a remote server and connecting it to Claude Desktop or Claude.ai.

---

## Understanding MCP Connection Types

### 1. **STDIO (Local) - What You're Using Now**
- Server runs on your local machine
- Claude Desktop communicates via standard input/output
- **Pros**: Simple, secure (no network exposure)
- **Cons**: Only works on your computer, can't share

### 2. **SSE (Server-Sent Events) - Remote Deployment**
- Server runs on a remote machine
- Claude connects via HTTP/HTTPS
- **Pros**: Can be shared, accessible from anywhere
- **Cons**: Requires server setup, authentication

### 3. **HTTP with MCP Gateway**
- Server exposed via HTTP API
- Claude connects through a gateway
- **Pros**: Most flexible, works with Claude.ai
- **Cons**: More complex setup

---

## Option 1: Deploy with SSE Transport (Recommended for Remote)

This is the most straightforward way to make your MCP server accessible remotely.

### Step 1: Modify Your Server for SSE

Update your `pdf_to_csv_server.py`:

```python
"""
PDF to CSV Converter MCP Server with SSE Transport
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Any
from pathlib import Path

import pdfplumber
import pandas as pd
from fastmcp import FastMCP

# ... (keep all your existing code)

# Create MCP server with SSE transport
mcp = FastMCP("pdf-to-csv")

# ... (keep all your existing tools)

if __name__ == "__main__":
    import sys

    # Check if running with --transport flag
    if "--sse" in sys.argv:
        # SSE mode for remote access
        print("Starting PDF to CSV MCP (SSE mode)...")
        print(f"- folder: {settings.folder}")
        print(f"- output: {settings.output_dir}")

        # Run with SSE transport on specific host/port
        mcp.run(transport="sse", host="0.0.0.0", port=8000)
    else:
        # STDIO mode for Claude Desktop
        print("Starting PDF to CSV MCP (STDIO mode)...")
        print(f"- folder: {settings.folder}")
        print(f"- output: {settings.output_dir}")
        mcp.run()
```

### Step 2: Test Locally First

```bash
# Activate virtual environment
source .venv/bin/activate

# Run in SSE mode
python pdf_to_csv_server.py --sse
```

You should see:
```
Starting PDF to CSV MCP (SSE mode)...
- folder: /path/to/pdfs
- output: /path/to/output_csv
Server running on http://0.0.0.0:8000
```

Test it:
```bash
curl http://localhost:8000/sse
```

### Step 3: Deploy to a Remote Server

#### Option A: Deploy to a VPS (DigitalOcean, AWS EC2, etc.)

**On your remote server:**

```bash
# 1. Install Python
sudo apt update
sudo apt install python3 python3-pip python3-venv -y

# 2. Create project directory
mkdir -p /opt/mcp-servers/pdf-to-csv
cd /opt/mcp-servers/pdf-to-csv

# 3. Upload your files (from local machine)
# Use scp, rsync, or git
```

**From your local machine:**
```bash
# Using scp
scp pdf_to_csv_server.py user@your-server.com:/opt/mcp-servers/pdf-to-csv/

# Or using rsync
rsync -av --exclude='.venv' --exclude='__pycache__' \
  /path/to/mcp-pdf-to-csv/ \
  user@your-server.com:/opt/mcp-servers/pdf-to-csv/
```

**Back on remote server:**
```bash
# 4. Set up virtual environment
cd /opt/mcp-servers/pdf-to-csv
python3 -m venv .venv
source .venv/bin/activate
pip install fastmcp pdfplumber pandas

# 5. Create directories
mkdir -p pdfs output_csv

# 6. Test the server
python pdf_to_csv_server.py --sse
```

### Step 4: Set Up as a Service (Keep Running)

Create a systemd service file:

```bash
sudo nano /etc/systemd/system/mcp-pdf-to-csv.service
```

Add this content:

```ini
[Unit]
Description=MCP PDF to CSV Server
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/mcp-servers/pdf-to-csv
Environment="PATH=/opt/mcp-servers/pdf-to-csv/.venv/bin"
ExecStart=/opt/mcp-servers/pdf-to-csv/.venv/bin/python pdf_to_csv_server.py --sse
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable mcp-pdf-to-csv
sudo systemctl start mcp-pdf-to-csv

# Check status
sudo systemctl status mcp-pdf-to-csv

# View logs
sudo journalctl -u mcp-pdf-to-csv -f
```

### Step 5: Set Up Reverse Proxy (Nginx)

**Install Nginx:**
```bash
sudo apt install nginx -y
```

**Create Nginx configuration:**
```bash
sudo nano /etc/nginx/sites-available/mcp-pdf-to-csv
```

Add this:
```nginx
server {
    listen 80;
    server_name mcp.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # SSE specific settings
        proxy_buffering off;
        proxy_cache off;
        proxy_read_timeout 86400;
    }
}
```

**Enable the site:**
```bash
sudo ln -s /etc/nginx/sites-available/mcp-pdf-to-csv /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Step 6: Add SSL with Let's Encrypt

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d mcp.yourdomain.com

# Test renewal
sudo certbot renew --dry-run
```

Now your server is accessible at: `https://mcp.yourdomain.com`

---

## Option 2: Using FastMCP Cloud (Easiest)

FastMCP offers a cloud hosting service that handles everything for you.

### Step 1: Sign Up for FastMCP Cloud

```bash
# Install FastMCP with cloud support
pip install fastmcp[cloud]

# Login to FastMCP Cloud
fastmcp login
```

### Step 2: Deploy Your Server

```bash
# From your project directory
fastmcp deploy

# Follow the prompts
# It will give you a URL like: https://your-server.fastmcp.cloud
```

### Step 3: Get Your API Key

```bash
fastmcp keys create --name "my-claude-connection"
# Save the API key securely
```

---

## Connecting Remote MCP to Claude Desktop

Once your server is deployed remotely, update your Claude Desktop config:

**Edit:** `~/Library/Application Support/Claude/claude_desktop_config.json`

### For SSE Server:

```json
{
  "mcpServers": {
    "pdf-to-csv-remote": {
      "url": "https://mcp.yourdomain.com/sse",
      "transport": "sse"
    }
  }
}
```

### With Authentication:

```json
{
  "mcpServers": {
    "pdf-to-csv-remote": {
      "url": "https://mcp.yourdomain.com/sse",
      "transport": "sse",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY_HERE"
      }
    }
  }
}
```

**Restart Claude Desktop** and your remote server will be available!

---

## Connecting to Claude.ai (Web Interface)

Currently, Claude.ai doesn't support direct MCP connections. However, there are workarounds:

### Option 1: Use MCP Gateway

Deploy an MCP Gateway that exposes your server as a REST API:

```bash
# Install MCP Gateway
npm install -g @modelcontextprotocol/gateway

# Run the gateway
mcp-gateway \
  --mcp-server http://localhost:8000/sse \
  --port 3000
```

Then use the gateway URL in your applications.

### Option 2: Create a Custom Claude Integration

Build a web interface that:
1. Connects to your MCP server
2. Accepts user input
3. Calls MCP tools
4. Returns results to Claude.ai via API

Example architecture:
```
Claude.ai API <-> Your Web App <-> MCP Server
```

---

## Security Considerations

### 1. Authentication

Add API key authentication to your server:

```python
from fastmcp import FastMCP
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                {"error": "Unauthorized"},
                status_code=401
            )

        token = auth_header.split(" ")[1]
        if token != "YOUR_SECRET_API_KEY":
            return JSONResponse(
                {"error": "Invalid token"},
                status_code=403
            )

        return await call_next(request)

# Create MCP with middleware
mcp = FastMCP(
    "pdf-to-csv",
    middleware=[Middleware(AuthMiddleware)]
)
```

### 2. Rate Limiting

```bash
# Install rate limiting
pip install slowapi
```

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)

mcp = FastMCP("pdf-to-csv")
mcp.app.state.limiter = limiter
mcp.app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@mcp.tool()
@limiter.limit("10/minute")
async def extract_tables(request, filename: str) -> str:
    """Rate-limited extraction."""
    # Your code
    pass
```

### 3. CORS (if needed for web access)

```python
from fastapi.middleware.cors import CORSMiddleware

mcp = FastMCP("pdf-to-csv")

mcp.app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://claude.ai"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Deployment Checklist

### Pre-Deployment
- [ ] Test server locally with `--sse` flag
- [ ] Test all tools work correctly
- [ ] Add error handling and logging
- [ ] Set up authentication
- [ ] Configure rate limiting
- [ ] Prepare environment variables

### Server Setup
- [ ] Choose hosting provider (AWS, DigitalOcean, etc.)
- [ ] Set up server with Python 3.14+
- [ ] Configure firewall (allow ports 80, 443, 8000)
- [ ] Install and configure Nginx
- [ ] Set up SSL certificate
- [ ] Create systemd service
- [ ] Test service starts on boot

### Post-Deployment
- [ ] Verify server is accessible via HTTPS
- [ ] Test MCP connection from Claude Desktop
- [ ] Monitor logs for errors
- [ ] Set up automatic backups
- [ ] Configure monitoring (uptime, errors)
- [ ] Document API keys and URLs

---

## Monitoring Your Remote Server

### 1. Basic Monitoring

```bash
# Watch logs in real-time
sudo journalctl -u mcp-pdf-to-csv -f

# Check service status
sudo systemctl status mcp-pdf-to-csv

# Check Nginx access logs
sudo tail -f /var/log/nginx/access.log

# Check Nginx error logs
sudo tail -f /var/log/nginx/error.log
```

### 2. Add Health Check Endpoint

```python
@mcp.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "folder": str(settings.folder),
        "output_dir": str(settings.output_dir),
        "pdfs_count": len(list_pdfs_in_folder(settings.folder))
    }
```

### 3. Set Up Uptime Monitoring

Use services like:
- **UptimeRobot** (free): https://uptimerobot.com
- **Pingdom**: https://pingdom.com
- **StatusCake**: https://statuscake.com

Configure to check: `https://mcp.yourdomain.com/health`

---

## Cost Estimates

### Self-Hosted on VPS
- **DigitalOcean Droplet**: $6-12/month
- **AWS EC2 t3.micro**: ~$8-10/month
- **Domain name**: $10-15/year
- **SSL certificate**: Free (Let's Encrypt)

**Total**: ~$10-15/month

### FastMCP Cloud
- Check current pricing at: https://fastmcp.cloud/pricing

---

## Complete Deployment Example

Here's a complete updated server file for remote deployment:

```python
"""
PDF to CSV Converter MCP Server
Supports both local (STDIO) and remote (SSE) deployment
"""

from __future__ import annotations
import sys
import os
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

# Helper functions
def list_pdfs_in_folder(folder: Path) -> List[str]:
    if not folder.is_dir():
        return []
    return sorted([
        p.name for p in folder.iterdir()
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXT
    ])

# ... (all your existing extraction functions)

# MCP Server
mcp = FastMCP("pdf-to-csv")

# Health check endpoint for remote deployment
@mcp.get("/health")
async def health_check():
    """Health check for monitoring."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "pdfs_available": len(list_pdfs_in_folder(settings.folder))
    }

# ... (all your existing tools)

# Main entry point
if __name__ == "__main__":
    # Get configuration from environment or args
    mode = os.getenv("MCP_TRANSPORT", "stdio")
    host = os.getenv("MCP_HOST", "0.0.0.0")
    port = int(os.getenv("MCP_PORT", "8000"))

    # Check command line args
    if "--sse" in sys.argv:
        mode = "sse"

    print(f"Starting PDF to CSV MCP Server...")
    print(f"- Mode: {mode}")
    print(f"- Folder: {settings.folder}")
    print(f"- Output: {settings.output_dir}")

    if mode == "sse":
        print(f"- Host: {host}")
        print(f"- Port: {port}")
        mcp.run(transport="sse", host=host, port=port)
    else:
        mcp.run()
```

**.env file for configuration:**
```bash
MCP_TRANSPORT=sse
MCP_HOST=0.0.0.0
MCP_PORT=8000
API_KEY=your-secret-api-key-here
```

---

## Quick Commands Reference

### Local Testing
```bash
# STDIO mode (for Claude Desktop)
python pdf_to_csv_server.py

# SSE mode (for remote)
python pdf_to_csv_server.py --sse
```

### Remote Server
```bash
# Start service
sudo systemctl start mcp-pdf-to-csv

# Stop service
sudo systemctl stop mcp-pdf-to-csv

# Restart service
sudo systemctl restart mcp-pdf-to-csv

# View logs
sudo journalctl -u mcp-pdf-to-csv -f

# Test health endpoint
curl https://mcp.yourdomain.com/health
```

---

## Summary

**Local Development (STDIO)**
- Simple, secure, local-only
- Perfect for personal use
- Current setup with Claude Desktop

**Remote Deployment (SSE)**
- Accessible from anywhere
- Requires server and domain
- Can be shared with others
- Needs authentication and SSL

**Next Steps:**
1. Decide if you need remote access
2. If yes, choose hosting provider
3. Follow deployment steps above
4. Update Claude Desktop config
5. Monitor and maintain

**Remember:** Always start with local testing before deploying remotely!
