# GitHub Setup Guide for AnalystKit

## 🚀 Ready to Push to GitHub!

Your AnalystKit package is now ready to be pushed to a private GitHub repository. Here's what to do:

## Step 1: Create GitHub Repository

1. Go to [GitHub.com](https://github.com)
2. Click "New repository" or "New"
3. Choose "Private repository"
4. Name it: `analystkit` (or `bitwise-analystkit`)
5. Description: "Shared Plotly theme, viz helpers, and settings for analytics projects"
6. **Don't** initialize with README, .gitignore, or license (we already have these)
7. Click "Create repository"

## Step 2: Connect and Push

After creating the repository, GitHub will show you commands. Use these:

```bash
# Add the remote origin (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/analystkit.git

# Push the main branch
git push -u origin main

# Push the tag
git push origin v1.0.0
```

## Step 3: Your Coworkers Install

Once pushed, your coworkers can install it with:

```bash
# Using pip
pip install git+https://github.com/YOUR_USERNAME/analystkit.git

# Using Poetry
poetry add git+https://github.com/YOUR_USERNAME/analystkit.git

# For specific version
pip install git+https://github.com/YOUR_USERNAME/analystkit.git@v1.0.0
```

## Step 4: Future Updates

When you make changes:

```bash
# Make your changes
git add .
git commit -m "Description of changes"
git push origin main

# Tag new version
git tag v1.1.0
git push origin v1.1.0
```

## 🔑 Important Notes

- **Keep it Private**: Since this contains your company's styling and potentially API keys
- **Update README**: Change `yourcompany` to your actual GitHub username in the README
- **Environment Variables**: Make sure `.env` is in `.gitignore` (it is!)
- **API Keys**: Never commit actual API keys, only the template

## 📋 Repository Structure

Your repository will contain:
- ✅ Complete Python package structure
- ✅ Custom fonts (Items-Regular.otf, PPNeueMontreal-Book.otf)
- ✅ Comprehensive styling and chart helpers
- ✅ Asset data fetching for crypto/indices
- ✅ Professional documentation
- ✅ MIT License
- ✅ Proper .gitignore

## 🎯 Next Steps

1. Create the GitHub repository
2. Push your code
3. Share the installation instructions with your team
4. Start using AnalystKit across your projects!

---

**Your AnalystKit is now a professional, distributable SDK! 🎉**
