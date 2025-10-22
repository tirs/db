# 🚀 Deploy to Streamlit Cloud - Quick Start

Your code is already pushed to GitHub at: **https://github.com/tirs/db**

## 3-Step Deployment:

### Step 1: Create Streamlit Cloud Account (2 min)
1. Go to https://streamlit.io/cloud
2. Click **"Sign up"**
3. Click **"Sign up with GitHub"**
4. Authorize Streamlit to access your repositories

### Step 2: Deploy Your App (1 min)
1. Once logged into Streamlit Cloud, click **"New app"**
2. Fill in:
   - **Repository**: `tirs/db`
   - **Branch**: `master`
   - **File path**: `streamlit_app.py`
3. Click **"Deploy!"**

Streamlit will build and launch your app automatically!

### Step 3: Share Link with Client
Your app will be live at:
```
https://db.streamlit.app
```

Share this link with your client - they can access the full dashboard!

---

## Optional: Use Custom Domain (db.syncronhub.com)

After app is deployed:

1. In Streamlit Cloud, go to app settings
2. Note your app URL
3. In Hostinger cPanel:
   - Go to **Zone Editor**
   - Add/Edit **CNAME** for `db`:
     - Name: `db`
     - Target: `db.streamlit.app`
   - Wait 15-30 min for DNS to update
4. Access at: `https://db.syncronhub.com`

---

## What Your Client Gets:

✅ **Search & Filter** - Find foods by name, category, calories  
✅ **Browse** - Explore all food categories  
✅ **Analysis** - Charts and nutrition statistics  
✅ **Top Foods** - Ranked by calories, protein, fiber  
✅ **Export** - Download data as CSV  
✅ **Responsive** - Works on mobile, tablet, desktop  

---

## Making Updates

After you deploy, any changes pushed to GitHub will auto-redeploy:

```bash
# Make changes locally
git add .
git commit -m "Your message"
git push origin master

# Streamlit Cloud automatically redeploys!
```

---

**Troubleshooting?** Check logs in Streamlit Cloud dashboard or read STREAMLIT_DEPLOYMENT.md