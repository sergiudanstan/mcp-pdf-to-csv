# Understanding Open Source Licenses for GitHub

A comprehensive guide to choosing and using licenses for your MCP server project.

---

## What is a License?

A **license** is a legal document that tells others:
- ✅ What they **CAN** do with your code
- ❌ What they **CANNOT** do with your code
- 📋 What **conditions** apply

**Without a license:** By default, you retain all rights and others legally cannot use, copy, or modify your code.

**With a license:** You explicitly grant permissions to others.

---

## Popular Open Source Licenses (Simple Comparison)

### 1. MIT License (RECOMMENDED - Already included!)

**What it means:**
- ✅ Anyone can use your code for **anything** (commercial, personal, etc.)
- ✅ Anyone can modify and distribute it
- ✅ Only requirement: Include the original license and copyright notice
- ❌ No warranty - you're not responsible if something breaks

**Best for:**
- Maximum sharing and adoption
- Want others to freely use your work
- Most popular for open source projects

**Famous projects using MIT:**
- React (Facebook)
- Node.js
- jQuery
- Rails

**Your current LICENSE file is MIT!** ✅

---

### 2. Apache 2.0 License

**What it means:**
- ✅ Similar to MIT (use, modify, distribute)
- ✅ **Extra**: Patent protection (protects users from patent lawsuits)
- ✅ Requires attribution and license notice
- ✅ Changes must be documented

**Best for:**
- Corporate/enterprise environments
- When patent protection matters
- Larger projects with contributions

**Famous projects:**
- Android
- Apache Server
- Kubernetes

---

### 3. GPL-3.0 (Copyleft)

**What it means:**
- ✅ Can use, modify, distribute
- ⚠️ **BUT**: Any derivative work MUST also be GPL-3.0
- ⚠️ Source code must be made available
- ⚠️ More restrictive than MIT

**Best for:**
- Want to ensure derivatives stay open source
- Philosophy of "free software"
- Prevent proprietary forks

**Famous projects:**
- Linux kernel
- WordPress
- GIMP

---

### 4. BSD 2-Clause / 3-Clause

**What it means:**
- ✅ Very similar to MIT
- ✅ Use, modify, distribute freely
- ✅ Slightly different legal wording

**Best for:**
- Academic projects
- Similar to MIT, personal preference

---

### 5. The Unlicense (Public Domain)

**What it means:**
- ✅ **No restrictions at all**
- ✅ Completely public domain
- ✅ Do whatever you want

**Best for:**
- Small utilities
- Want zero restrictions
- Don't care about attribution

---

## License Comparison Table

| License | Can Use Commercially? | Can Modify? | Can Distribute? | Must Share Source? | Must Include License? | Patent Grant? |
|---------|----------------------|-------------|-----------------|--------------------|-----------------------|---------------|
| **MIT** | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No | ✅ Yes | ❌ No |
| **Apache 2.0** | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No | ✅ Yes | ✅ Yes |
| **GPL-3.0** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ **Yes** | ✅ Yes | ✅ Yes |
| **BSD** | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No | ✅ Yes | ❌ No |
| **Unlicense** | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No | ❌ No | ❌ No |

---

## How to Choose a License

### Decision Tree

**Q1: Do you want others to use your code freely?**
- **No** → Don't use a license (all rights reserved) or use a restrictive license
- **Yes** → Continue to Q2

**Q2: Do you care if companies make money from your code without giving back?**
- **Yes, I want them to share back** → **GPL-3.0**
- **No, they can do whatever** → Continue to Q3

**Q3: Do you need patent protection?**
- **Yes** → **Apache 2.0**
- **No** → Continue to Q4

**Q4: Do you want maximum adoption and simplicity?**
- **Yes** → **MIT License** ⭐ (RECOMMENDED)
- **Don't care about attribution** → **Unlicense**

### For Your MCP Server Project

**I recommend MIT License** (already included!) because:
1. ✅ Most popular and widely understood
2. ✅ Simple and permissive
3. ✅ Companies and individuals can use it freely
4. ✅ Maximum adoption potential
5. ✅ Standard for FastMCP projects

---

## How to Add a License on GitHub

### Method 1: When Creating Repository (Easiest)

When you create the repository:

1. Check **"Add a license"** (bottom of the form)
2. Choose from the dropdown:
   - **MIT License** (recommended)
   - Apache License 2.0
   - GNU GPLv3
   - BSD 2-Clause / 3-Clause
   - The Unlicense
   - And more...
3. GitHub will automatically create the LICENSE file

**You already have a LICENSE file, so you can skip this!** ✅

---

### Method 2: Add License After Creating Repository

**Via GitHub Website:**

1. Go to your repository on GitHub
2. Click **"Add file"** → **"Create new file"**
3. Name it: `LICENSE`
4. Click **"Choose a license template"** button on the right
5. Select your license (e.g., MIT License)
6. GitHub auto-fills with the correct text
7. Fill in the year and your name
8. Click **"Commit new file"**

---

### Method 3: Manually (You Already Did This!)

You already have a `LICENSE` file with MIT License!

Check it:
```bash
cat LICENSE
```

If you want to change it, just replace the content with a different license from https://choosealicense.com

---

## What's in Your Current LICENSE File

```
MIT License

Copyright (c) 2025 MCP PDF to CSV Server Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

[... full MIT License text ...]
```

**This means:**
- ✅ Anyone can use your code for free
- ✅ Anyone can modify it
- ✅ Anyone can sell products using it
- ✅ They just need to include this license text
- ✅ No warranty (you're not liable if something breaks)

---

## How GitHub Displays Licenses

### Repository Badge

GitHub automatically:
1. **Detects** your LICENSE file
2. **Shows** a badge on your repository
3. **Displays** license info in the sidebar

**Example:**
```
About
FastMCP server for extracting tables from PDF files

📋 MIT License
⭐ Stars
🔀 Forks
```

### In Search Results

GitHub shows your license type in search results, making it easy for others to find permissively-licensed projects.

---

## License Best Practices

### 1. Always Include a License

**Why?**
- Without one, others legally can't use your code
- Shows professionalism
- Clarifies usage rights

### 2. Add License Badge to README

Add this to your `README.md`:

```markdown
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

Or with a badge:

```markdown
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
```

### 3. Keep License File in Root

- Name it `LICENSE` (no extension) or `LICENSE.txt`
- Keep it in the root directory
- Don't modify the standard text

### 4. Update Copyright Year

When you make changes in a new year:
```
Copyright (c) 2025-2026 MCP PDF to CSV Server Contributors
```

---

## Changing Your License

### If You Want to Change (Not Recommended After Publishing)

**Before pushing to GitHub:**
```bash
# Replace LICENSE file content
# Visit https://choosealicense.com/licenses/
# Copy the license text you want
# Save to LICENSE file

git add LICENSE
git commit -m "Change license to Apache 2.0"
git push
```

**After others are using it:**
- ⚠️ **Difficult** - others may have rights under old license
- Need permission from all contributors
- Generally: **Don't change licenses after release**

---

## Special Cases

### Dual Licensing

You can offer multiple licenses:

```markdown
## License

This project is dual-licensed under:
- MIT License (for open source use)
- Commercial License (for proprietary use)

See LICENSE-MIT and LICENSE-COMMERCIAL for details.
```

### No License

If you don't want to share:
```markdown
## License

Copyright (c) 2025 Your Name. All rights reserved.

This software is proprietary and may not be used, copied, or distributed
without express written permission.
```

---

## FAQ

### Q: Can I use multiple licenses?

**A:** Yes (dual licensing), but it's complex. Stick with one for simplicity.

### Q: What if I don't add a license?

**A:** By default, you retain all rights. Others cannot legally use your code, even if it's public on GitHub.

### Q: Can I change the license later?

**A:** Difficult after others use it. Choose carefully from the start.

### Q: Does GitHub enforce licenses?

**A:** No, GitHub just hosts the code. The license is a legal agreement between you and users.

### Q: Can companies use my MIT licensed code?

**A:** Yes! That's the point. They can even sell products using it. They just need to include your license text.

### Q: Am I liable if my code breaks something?

**A:** No! MIT (and most open source licenses) include "no warranty" clauses protecting you.

---

## Quick Reference

### For Your MCP Server (Current Setup)

**You have:** MIT License ✅

**This means users can:**
- ✅ Use it commercially
- ✅ Modify it
- ✅ Distribute it
- ✅ Sublicense it
- ✅ Use it privately

**Users must:**
- ✅ Include your license and copyright notice
- ✅ Not hold you liable

**Perfect for:**
- Open source sharing
- Maximum adoption
- Standard practice

---

## Resources

- **Choose a License:** https://choosealicense.com/
- **GitHub Licensing:** https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository
- **MIT License:** https://opensource.org/licenses/MIT
- **TL;DR Legal:** https://www.tldrlegal.com/ (Plain English explanations)

---

## Summary

**Your current setup:**
- ✅ MIT License already added to your project
- ✅ Perfect choice for MCP server
- ✅ Ready for GitHub
- ✅ No action needed!

**When you push to GitHub:**
1. GitHub will automatically detect your LICENSE file
2. Show "MIT License" badge on your repo
3. Others can freely use and contribute

**You're all set!** 🎉

The MIT License is the standard for open source projects like yours and requires no additional configuration on GitHub.
