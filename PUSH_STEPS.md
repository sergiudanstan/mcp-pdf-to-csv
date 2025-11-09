# Push to GitHub - Simple Steps

Follow these commands exactly in order.

---

## Step 1: Configure Git (First Time Only)

Replace `Your Name` and `your-email@example.com` with your actual information:

```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

**Verify it worked:**
```bash
git config --global --list
```

---

## Step 2: Add New Files

```bash
cd /Users/sara/MCP_PDF_CSV

# Add all new files
git add .

# Check what will be committed
git status
```

You should see files like:
- LICENSE
- GITHUB_READY.md
- LICENSE_GUIDE.md
- And more...

---

## Step 3: Commit the Changes

```bash
git commit -m "Add license and GitHub deployment documentation"
```

---

## Step 4: Create Repository on GitHub

**Open your browser and go to:**
https://github.com/new

**Fill in:**
- Repository name: `mcp-pdf-to-csv`
- Description: `FastMCP server for extracting tables from PDF files to CSV format`
- Choose: **Public** (recommended) or **Private**

**IMPORTANT - Do NOT check these:**
- ☐ Add a README file
- ☐ Add .gitignore
- ☐ Choose a license

**Click:** "Create repository"

---

## Step 5: Connect to Your Repository

**Replace `YOUR_USERNAME` with your actual GitHub username:**

```bash
git remote add origin https://github.com/YOUR_USERNAME/mcp-pdf-to-csv.git

# Verify
git remote -v
```

---

## Step 6: Push Your Code

```bash
git push -u origin main
```

**If you get an authentication error**, GitHub will prompt you for credentials:
- **Username:** Your GitHub username
- **Password:** Use a Personal Access Token (NOT your password!)

---

## Getting a Personal Access Token

If you need a token:

1. Go to: https://github.com/settings/tokens
2. Click: "Generate new token" → "Generate new token (classic)"
3. Name: `MCP Server`
4. Expiration: `90 days` (or your choice)
5. Select scopes: ✓ **repo** (check all repo boxes)
6. Click: "Generate token"
7. **COPY THE TOKEN** (you'll only see it once!)
8. Use this token as your password when pushing

---

## Step 7: Verify Success

Visit your repository:
```
https://github.com/YOUR_USERNAME/mcp-pdf-to-csv
```

You should see:
- ✅ All your files
- ✅ README.md displayed
- ✅ "📋 MIT License" badge on the right

---

## Troubleshooting

### Authentication Failed

**Problem:** `Authentication failed`

**Solution:** Use Personal Access Token (see above)

---

### Remote Already Exists

**Problem:** `remote origin already exists`

**Solution:**
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/mcp-pdf-to-csv.git
```

---

### Wrong Username/Email in Commit

**Problem:** Commit shows wrong author

**Solution:**
```bash
git commit --amend --reset-author --no-edit
git push --force origin main
```

---

## Quick Command Summary

```bash
# 1. Configure (once)
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# 2. Add and commit
git add .
git commit -m "Add license and GitHub documentation"

# 3. Connect to GitHub (after creating repo)
git remote add origin https://github.com/YOUR_USERNAME/mcp-pdf-to-csv.git

# 4. Push
git push -u origin main
```

---

## Alternative: Interactive Script

Run the interactive script that guides you through each step:

```bash
./PUSH_TO_GITHUB.sh
```

This script will:
- Configure git interactively
- Add and commit files
- Guide you through GitHub setup
- Push your code

---

## After Successful Push

1. **Visit your repository** on GitHub
2. **Add topics** (Settings → About → Topics):
   - `mcp`
   - `claude`
   - `pdf`
   - `csv`
   - `fastmcp`
   - `python`
3. **Star your own repo** (shows you care!)
4. **Share it** with others

---

**You're ready! Start with Step 1 and work your way through.** 🚀
