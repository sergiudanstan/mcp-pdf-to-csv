# GitHub Setup Commands

Quick reference for deploying your MCP server to GitHub.

---

## Step 1: Configure Git (First Time Only)

Set your name and email for git commits:

```bash
# Set your GitHub username
git config --global user.name "Your Name"

# Set your GitHub email
git config --global user.email "your-email@example.com"

# Verify
git config --global --list
```

If you want to update the initial commit with your info:

```bash
git commit --amend --reset-author --no-edit
```

---

## Step 2: Create GitHub Repository

### Option A: Via GitHub Website (Recommended)

1. Go to **https://github.com/new**
2. Repository name: `mcp-pdf-to-csv`
3. Description: `FastMCP server for extracting tables from PDF files to CSV format`
4. Choose **Public** or **Private**
5. **Do NOT** check "Add a README" (you already have one)
6. **Do NOT** add .gitignore (you already have one)
7. Choose License: **MIT License** (recommended)
8. Click **Create repository**

### Option B: Via GitHub CLI

```bash
# Install GitHub CLI (if not installed)
brew install gh

# Login to GitHub
gh auth login

# Create and push repository
gh repo create mcp-pdf-to-csv \
  --public \
  --description "FastMCP server for extracting tables from PDF files to CSV format" \
  --source=. \
  --push
```

---

## Step 3: Connect to GitHub (If using Option A)

After creating the repository on GitHub, run these commands:

```bash
# Add GitHub as remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/mcp-pdf-to-csv.git

# Verify remote
git remote -v

# Push to GitHub
git push -u origin main
```

**Replace `YOUR_USERNAME` with your actual GitHub username!**

---

## Step 4: Verify Upload

Visit your repository:
```
https://github.com/YOUR_USERNAME/mcp-pdf-to-csv
```

You should see all your files! ✅

---

## Future Updates

When you make changes:

```bash
# 1. Check what changed
git status

# 2. Stage all changes
git add .

# 3. Commit with message
git commit -m "Add new feature or fix"

# 4. Push to GitHub
git push
```

---

## Current Status

✅ Git repository initialized
✅ Initial commit created (14 files, 3359+ insertions)
✅ Ready to push to GitHub

**Files committed:**
- pdf_to_csv_server.py
- All documentation (.md files)
- requirements.txt
- .gitignore
- Directory structure

**Files ignored:**
- .venv/ (virtual environment)
- __pycache__/ (Python cache)
- *.pdf (user PDFs)
- *.csv (generated CSVs)
- Test files

---

## Troubleshooting

### Authentication Error

If you get authentication errors when pushing:

**Using Personal Access Token:**
```bash
# Create token at: https://github.com/settings/tokens
# When prompted for password, use the token instead
```

**Using SSH (Recommended):**
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Copy public key
cat ~/.ssh/id_ed25519.pub

# Add to GitHub: Settings → SSH and GPG keys
# https://github.com/settings/keys

# Change remote to SSH
git remote set-url origin git@github.com:YOUR_USERNAME/mcp-pdf-to-csv.git

# Test connection
ssh -T git@github.com

# Push
git push -u origin main
```

### Wrong Author Name

```bash
# Fix the last commit
git commit --amend --author="Your Name <your-email@example.com>" --no-edit

# Force push (only if not shared yet)
git push --force origin main
```

---

## Quick Reference

```bash
# Status
git status                    # Check current status
git log --oneline            # View commit history

# Changes
git diff                     # View unstaged changes
git diff --staged            # View staged changes

# Commit
git add .                    # Stage all changes
git commit -m "Message"      # Commit changes
git push                     # Push to GitHub

# Undo
git restore file.py          # Discard changes
git reset HEAD~1             # Undo last commit
```

---

## Next Steps

1. **Configure git** (set your name/email)
2. **Create GitHub repository** (via website or CLI)
3. **Connect and push** (add remote and push)
4. **Share your project!** 🎉

Your repository will be at:
**https://github.com/YOUR_USERNAME/mcp-pdf-to-csv**
