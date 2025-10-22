# 🚀 Streamlit App Deployment Guide

Deploy your Nutrition Database to Streamlit Cloud for free!

## Prerequisites

- GitHub account
- Streamlit Cloud account (free at https://streamlit.io/cloud)

## Step 1: Initialize Git & Push to GitHub

```bash
cd c:\Users\simba\Desktop\Database

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Nutrition Database with Streamlit app"

# Add remote repository (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 2: Create Streamlit Cloud Account

1. Go to https://streamlit.io/cloud
2. Click "Sign up"
3. Choose "Sign up with GitHub"
4. Authorize Streamlit to access your GitHub repositories

## Step 3: Deploy on Streamlit Cloud

1. After signing in to Streamlit Cloud, click "New app"
2. Fill in:
   - **Repository**: YOUR_USERNAME/REPO_NAME
   - **Branch**: main
   - **File path**: streamlit_app.py
3. Click "Deploy!"

Streamlit will automatically install dependencies from `requirements.txt` and start the app.

Your app will be live at: `https://REPO_NAME.streamlit.app`

## Step 4: Share with Client at Custom Domain

To use your custom domain `db.syncronhub.com`:

### Option A: DNS CNAME (Recommended)

1. In Streamlit Cloud app settings, get your app's URL
2. In Hostinger cPanel:
   - Go to **Zone Editor**
   - Add CNAME record:
     - Name: `db`
     - Type: CNAME
     - Value: `REPO_NAME.streamlit.app`
   - Wait 15-30 minutes for DNS to propagate

3. Access at: `https://db.syncronhub.com`

### Option B: Share Direct Link

Simply share `https://REPO_NAME.streamlit.app` with your client

## Step 5: Environment Variables (Optional)

If you don't want to hardcode database credentials, use Streamlit secrets:

1. In Streamlit Cloud dashboard, click "Manage secrets"
2. Add your credentials as secrets:
```
DB_HOST = "82.197.82.46"
DB_USER = "u280406916_nutrition"
DB_PASSWORD = "your_password"
DB_NAME = "u280406916_nutrition"
```

3. Update `streamlit_app.py` to use secrets:
```python
import streamlit as st

DB_CONFIG = {
    'host': st.secrets["DB_HOST"],
    'user': st.secrets["DB_USER"],
    'password': st.secrets["DB_PASSWORD"],
    'database': st.secrets["DB_NAME"],
    'port': 3306
}
```

## Troubleshooting

### App won't deploy?
- Check `requirements.txt` syntax
- Ensure `streamlit_app.py` exists in repository root
- Check Streamlit Cloud logs for errors

### Slow database queries?
- Streamlit caches queries with `@st.cache_data`
- Add `ttl=600` to cache decorator to refresh data every 10 minutes

### Database connection errors?
- Verify database credentials in secrets
- Ensure database allows external connections from Streamlit servers

## File Structure

```
Database/
├── streamlit_app.py          # Main Streamlit app
├── app.py                    # Flask app (optional)
├── requirements.txt          # Python dependencies
├── README.md
├── STREAMLIT_DEPLOYMENT.md   # This file
├── templates/
│   └── index.html           # Flask template (optional)
└── [other files]
```

## Making Updates

Simply push updates to GitHub, and Streamlit Cloud will automatically redeploy!

```bash
git add .
git commit -m "Update description"
git push origin main
```

---

**Need help?** Check Streamlit docs: https://docs.streamlit.io/