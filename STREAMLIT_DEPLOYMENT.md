# 🚀 Streamlit Cloud Deployment Guide

## Prerequisites

1. **Streamlit Cloud Account** - Sign up at https://streamlit.io/cloud
2. **GitHub Repository** - Push your code to GitHub
3. **Google Gemini API Key** - Get it from https://ai.google.dev/

## Step 1: Get Your Gemini API Key

1. Go to **https://ai.google.dev/**
2. Click **"Get API Key"** button
3. Select or create a Google Cloud project
4. Create an API key for Gemini
5. Copy the API key (you'll need it for step 3)

## Step 2: Deploy on Streamlit Cloud

1. Go to **https://share.streamlit.io**
2. Click **"Create app"**
3. Select your GitHub repository
4. Select the branch (usually `main`)
5. Set the main file path to `app.py`
6. Click **"Deploy"**

## Step 3: Add Secrets (IMPORTANT!)

After deployment, you must add your API key as a secret:

1. In your Streamlit Cloud app, click the **three dots (⋮)** in top-right
2. Click **"Settings"**
3. Go to **"Secrets"** tab
4. Add this configuration:

```toml
GEMINI_API_KEY = "your-actual-api-key-here"
```

5. Click **"Save"**
6. The app will automatically redeploy

## Step 4: Verify Deployment

1. Wait for the app to redeploy (green status bar)
2. Try sending a message in the Claim Assistant
3. If it works, you're good to go! ✅

## 🔧 Local Development Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root:
```
GEMINI_API_KEY=your-actual-api-key-here
```

Or use `.streamlit/secrets.toml` for local Streamlit:
```toml
GEMINI_API_KEY = "your-actual-api-key-here"
```

### 3. Run Locally
```bash
python -m streamlit run app.py
```

## 📋 File Structure for Secrets

**For Streamlit Cloud:**
- Use the app settings → Secrets tab
- Format: TOML (same as secrets.toml)

**For Local Development:**
- `.env` file (git-ignored)
- `.streamlit/secrets.toml` (git-ignored)

## ⚠️ Important Notes

- **Never commit actual API keys** to GitHub
- `.env` and `secrets.toml` are in `.gitignore`
- Streamlit Cloud reads secrets from settings, not from files
- The app will show a clear error if API key is missing
- Each environment (local, cloud) needs its own secrets

## 🔐 Security Best Practices

1. ✅ Use Streamlit Cloud Secrets for production
2. ✅ Use `.env` file locally (git-ignored)
3. ✅ Never commit credentials to git
4. ✅ Rotate API keys regularly
5. ✅ Use minimal required permissions for API keys
6. ✅ Monitor API usage in Google Cloud console

## 🆘 Troubleshooting

### Error: "GEMINI_API_KEY not found"
**Solution:** 
- Make sure you added the secret in Streamlit Cloud settings
- If local, check `.env` or `.streamlit/secrets.toml` exists
- Verify the exact key name is `GEMINI_API_KEY`

### Error: "Failed to initialize Gemini client"
**Solution:**
- Verify your API key is valid and active
- Check Google Cloud console for API quotas
- Ensure Generative AI API is enabled in Google Cloud

### App deploys but assistant doesn't respond
**Solution:**
- Check the Streamlit Cloud logs (click app name → Logs)
- Verify API key is correctly set in Secrets
- Try refreshing the page
- Check API usage limits in Google Cloud

### Secrets not updating
**Solution:**
- Click "Rerun" button in app
- Or re-deploy from Streamlit Cloud dashboard
- Secrets take effect on next app rerun

## 📚 Additional Resources

- [Streamlit Cloud Docs](https://docs.streamlit.io/deploy/streamlit-community-cloud)
- [Streamlit Secrets Management](https://docs.streamlit.io/develop/api-reference/connections/st.secrets)
- [Google Gemini API Docs](https://ai.google.dev/docs)
- [Requirements.txt Setup](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app#create-your-requirements-file)

---

## ✅ Deployment Checklist

- [ ] Gemini API key obtained
- [ ] Code pushed to GitHub
- [ ] Repository is public or you have access
- [ ] Streamlit Cloud app created
- [ ] API key added to Secrets
- [ ] App redeployed
- [ ] Assistant feature tested and working
- [ ] No errors in logs

---

**Your app is now ready for production!** 🎉
