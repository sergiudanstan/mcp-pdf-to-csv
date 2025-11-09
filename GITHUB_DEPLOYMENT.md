# Deploying MCP Server to GitHub

Complete guide for publishing your PDF to CSV MCP server on GitHub.

---

## Why Deploy to GitHub?

### Benefits
✅ **Version Control** - Track changes and history
✅ **Backup** - Safe storage in the cloud
✅ **Sharing** - Others can use your server
✅ **Collaboration** - Accept contributions
✅ **Portfolio** - Showcase your work
✅ **Easy Installation** - Clone and run anywhere

---

## Part 1: Prepare Your Repository

### Step 1: Check What Will Be Committed

We've already created a `.gitignore` file that excludes:
- Virtual environment (`.venv/`)
- Python cache (`__pycache__/`)
- IDE files (`.vscode/`, `.DS_Store`)
- Local PDFs and CSVs (user data)
- Test files

**What WILL be committed:**
- ✅ `pdf_to_csv_server.py` - Main server code
- ✅ Documentation (all `.md` files)
- ✅ `requirements.txt` - Dependencies
- ✅ `.gitignore` - Git configuration
- ✅ Directory structure (via `.gitkeep` files)

### Step 2: Create requirements.txt

This file lists all Python dependencies:

```bash
# Create requirements file from current environment
source .venv/bin/activate
pip freeze > requirements.txt
```

Or manually create with just the essentials:

```txt
fastmcp>=2.13.0
pdfplumber>=0.11.0
pandas>=2.3.0
```

---

## Part 2: Initialize Git Repository

### Step 3: Initialize Git

```bash
cd /Users/sara/MCP_PDF_CSV

# Initialize git repository
git init

# Check status
git status
```

You should see all the files that will be tracked.

### Step 4: Make Initial Commit

```bash
# Add all files
git add .

# Check what's staged
git status

# Make your first commit
git commit -m "Initial commit: PDF to CSV MCP Server

- FastMCP server for extracting tables from PDFs
- Supports multiple extraction strategies (auto, lattice, stream)
- Complete documentation for local and remote deployment
- 6 MCP tools: set_folder, set_output, list_pdfs, extract_tables, extract_all, show_config"
```

---

## Part 3: Create GitHub Repository

### Step 5: Create Repository on GitHub

**Option A: Via GitHub Website (Easier)**

1. Go to https://github.com
2. Click the **"+"** icon → **"New repository"**
3. Fill in details:
   - **Repository name:** `mcp-pdf-to-csv` (or your choice)
   - **Description:** `FastMCP server for extracting tables from PDF files to CSV format`
   - **Visibility:**
     - **Public** - Anyone can see (recommended for sharing)
     - **Private** - Only you can see
   - **Initialize:**
     - ❌ Do NOT check "Add README" (you already have one)
     - ❌ Do NOT add .gitignore (you already have one)
     - ✅ Choose a license (MIT recommended)
4. Click **"Create repository"**

**Option B: Via GitHub CLI (If you have it)**

```bash
# Install GitHub CLI (if needed)
brew install gh

# Login
gh auth login

# Create repository
gh repo create mcp-pdf-to-csv \
  --public \
  --description "FastMCP server for extracting tables from PDF files to CSV format" \
  --source=. \
  --push
```

### Step 6: Connect Local Repository to GitHub

After creating the repository on GitHub, you'll see commands like:

```bash
# Add GitHub as remote
git remote add origin https://github.com/YOUR_USERNAME/mcp-pdf-to-csv.git

# Verify remote
git remote -v

# Push to GitHub
git branch -M main
git push -u origin main
```

**Replace `YOUR_USERNAME`** with your actual GitHub username.

---

## Part 4: Push Your Code

### Step 7: Push to GitHub

```bash
# Push your code
git push -u origin main
```

Your code is now on GitHub! 🎉

Visit: `https://github.com/YOUR_USERNAME/mcp-pdf-to-csv`

---

## Part 5: Make Your Repository User-Friendly

### Step 8: Add a Great README

Update your `README.md` to include:

1. **Project Title & Description**
2. **Installation Instructions**
3. **Quick Start Guide**
4. **Usage Examples**
5. **Configuration**
6. **Contributing Guidelines**
7. **License**

Example structure:

```markdown
# PDF to CSV MCP Server

FastMCP server for extracting tables from PDF files and converting them to CSV format.

## Features
- 🔄 Batch PDF processing
- 📊 Multiple extraction strategies (auto, lattice, stream)
- 🎯 Page-specific extraction
- 📁 Configurable input/output folders
- 🔗 Works with Claude Desktop

## Installation

### Clone the repository
\`\`\`bash
git clone https://github.com/YOUR_USERNAME/mcp-pdf-to-csv.git
cd mcp-pdf-to-csv
\`\`\`

### Set up virtual environment
\`\`\`bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
\`\`\`

### Install dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

## Quick Start

### 1. Run the server
\`\`\`bash
python pdf_to_csv_server.py
\`\`\`

### 2. Configure Claude Desktop

Add to \`~/Library/Application Support/Claude/claude_desktop_config.json\`:

\`\`\`json
{
  "mcpServers": {
    "pdf-to-csv": {
      "command": "/FULL/PATH/TO/mcp-pdf-to-csv/.venv/bin/python3",
      "args": ["/FULL/PATH/TO/mcp-pdf-to-csv/pdf_to_csv_server.py"]
    }
  }
}
\`\`\`

### 3. Use in Claude Desktop

Ask Claude:
- "Use pdf-to-csv to list PDFs"
- "Extract tables from myfile.pdf"

## Documentation

- [Complete Development Guide](MCP_DEVELOPMENT_GUIDE.md)
- [Remote Deployment Guide](REMOTE_DEPLOYMENT_GUIDE.md)
- [Quick Start](QUICK_START.md)

## License

MIT License - see [LICENSE](LICENSE) file
```

### Step 9: Add Topics/Tags

On GitHub repository page:
1. Click the **⚙️ gear** icon next to "About"
2. Add topics:
   - `mcp`
   - `claude`
   - `pdf`
   - `csv`
   - `fastmcp`
   - `table-extraction`
   - `python`

### Step 10: Add GitHub Actions (Optional)

Create `.github/workflows/test.yml` for automated testing:

```yaml
name: Test MCP Server

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.14'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Test server
        run: |
          python test_server.py
```

---

## Part 6: Usage Instructions for Others

### For Someone Cloning Your Repository

**They will run:**

```bash
# 1. Clone your repository
git clone https://github.com/YOUR_USERNAME/mcp-pdf-to-csv.git
cd mcp-pdf-to-csv

# 2. Set up environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Add to Claude Desktop config
# Edit: ~/Library/Application Support/Claude/claude_desktop_config.json
{
  "mcpServers": {
    "pdf-to-csv": {
      "command": "/absolute/path/to/mcp-pdf-to-csv/.venv/bin/python3",
      "args": ["/absolute/path/to/mcp-pdf-to-csv/pdf_to_csv_server.py"]
    }
  }
}

# 4. Restart Claude Desktop
```

---

## Part 7: Keeping Your Repository Updated

### Making Changes

```bash
# 1. Make your changes to files
# Edit pdf_to_csv_server.py or documentation

# 2. Check what changed
git status
git diff

# 3. Stage changes
git add .

# 4. Commit with descriptive message
git commit -m "Add support for merged CSV output"

# 5. Push to GitHub
git push
```

### Best Practices for Commit Messages

**Good:**
```
✅ "Add rate limiting to extraction tools"
✅ "Fix pdfplumber API compatibility issue"
✅ "Update documentation with remote deployment guide"
```

**Bad:**
```
❌ "update"
❌ "fix stuff"
❌ "changes"
```

---

## Part 8: Advanced GitHub Features

### Add a License

Choose a license for your project:

**MIT License** (Recommended - very permissive):
```bash
# GitHub will help you add this during repository creation
# Or add manually as LICENSE file
```

**Common licenses:**
- **MIT** - Anyone can do almost anything
- **Apache 2.0** - Similar to MIT, with patent protection
- **GPL-3.0** - Requires derivative works to be open source

### Create Issues and Pull Requests

**Issues** - Track bugs and feature requests:
- Go to "Issues" tab → "New issue"
- Describe the problem or feature
- Add labels (bug, enhancement, documentation)

**Pull Requests** - Propose changes:
1. Fork the repository
2. Make changes in a branch
3. Submit pull request
4. Review and merge

### Add GitHub Pages (Project Website)

Create a website for your project:

1. Go to Settings → Pages
2. Source: Deploy from branch `main` → `/docs` or `/`
3. Your site will be at: `https://YOUR_USERNAME.github.io/mcp-pdf-to-csv/`

---

## Part 9: Collaboration Features

### Allow Others to Contribute

**Make it easy for others:**

1. **Create CONTRIBUTING.md:**
```markdown
# Contributing to PDF to CSV MCP Server

## How to Contribute

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test: `python test_server.py`
5. Commit: `git commit -m "Add feature"`
6. Push: `git push origin feature-name`
7. Create Pull Request

## Development Setup

\`\`\`bash
git clone https://github.com/YOUR_USERNAME/mcp-pdf-to-csv.git
cd mcp-pdf-to-csv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
\`\`\`

## Code Style

- Follow PEP 8
- Add docstrings to all functions
- Update documentation for new features
```

2. **Add CODE_OF_CONDUCT.md** (GitHub provides templates)

### Protect Your Main Branch

Settings → Branches → Add rule:
- Require pull request reviews
- Require status checks to pass
- No force pushes

---

## Part 10: Repository Structure

### Your Final Structure

```
mcp-pdf-to-csv/
├── .github/
│   └── workflows/
│       └── test.yml              # GitHub Actions
├── pdfs/
│   └── .gitkeep                  # Keep directory in git
├── output_csv/
│   └── .gitkeep                  # Keep directory in git
├── .gitignore                    # Git ignore rules
├── pdf_to_csv_server.py          # Main server
├── requirements.txt              # Python dependencies
├── README.md                     # Main documentation
├── LICENSE                       # License file
├── CONTRIBUTING.md               # Contribution guidelines
├── MCP_DEVELOPMENT_GUIDE.md      # Development guide
├── REMOTE_DEPLOYMENT_GUIDE.md    # Deployment guide
├── DEPLOYMENT_COMPARISON.md      # Comparison guide
├── DEPLOYMENT_SUMMARY.md         # Summary
├── QUICK_START.md                # Quick reference
├── INDEX.md                      # Documentation index
└── GITHUB_DEPLOYMENT.md          # This file
```

---

## Quick Command Reference

### Initial Setup
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/mcp-pdf-to-csv.git
git push -u origin main
```

### Regular Updates
```bash
git status                    # Check changes
git add .                     # Stage all changes
git commit -m "Description"   # Commit changes
git push                      # Push to GitHub
```

### Branching
```bash
git checkout -b feature-name  # Create branch
git checkout main             # Switch to main
git merge feature-name        # Merge branch
git branch -d feature-name    # Delete branch
```

### Undoing Changes
```bash
git restore file.py           # Discard changes to file
git reset HEAD~1              # Undo last commit (keep changes)
git revert <commit-hash>      # Revert a specific commit
```

---

## Troubleshooting

### Large Files Error

If you accidentally try to commit large PDFs:

```bash
# Remove from staging
git rm --cached pdfs/*.pdf

# Make sure .gitignore includes them
echo "pdfs/*.pdf" >> .gitignore

# Commit the changes
git add .gitignore
git commit -m "Update .gitignore to exclude PDFs"
```

### Authentication Issues

**Using HTTPS:**
```bash
# GitHub now requires personal access tokens
# Create one at: https://github.com/settings/tokens
# Use token as password when pushing
```

**Using SSH (Recommended):**
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add to GitHub: Settings → SSH and GPG keys
cat ~/.ssh/id_ed25519.pub

# Change remote to SSH
git remote set-url origin git@github.com:YOUR_USERNAME/mcp-pdf-to-csv.git
```

---

## Summary

**Benefits of GitHub Deployment:**
- ✅ Version control and history
- ✅ Cloud backup
- ✅ Easy sharing and installation
- ✅ Collaboration features
- ✅ Professional portfolio piece

**Your Repository URL:**
`https://github.com/YOUR_USERNAME/mcp-pdf-to-csv`

**For Others to Use:**
```bash
git clone https://github.com/YOUR_USERNAME/mcp-pdf-to-csv.git
cd mcp-pdf-to-csv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Next Steps:**
1. Create requirements.txt
2. Initialize git repository
3. Create GitHub repository
4. Push your code
5. Share with the world! 🚀
