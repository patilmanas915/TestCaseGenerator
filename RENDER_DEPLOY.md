# 🚀 Render Deployment Guide for AI Test Case Generator

## Quick Deploy to Render (Free) - FIXED VERSION

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Fix Render deployment - Python 3.11 + minimal dependencies"
git push origin main
```

### Step 2: Deploy on Render
1. **Go to [render.com](https://render.com) and sign up**
2. **Click "New +" → "Web Service"**
3. **Connect your GitHub repository: `TestCaseGenerator`**

### Step 3: Configure Deployment (UPDATED)
**Service Configuration:**
- **Name**: `ai-testcase-generator`
- **Environment**: `Python 3`
- **Runtime**: `Python 3.11.9`
- **Build Command**: 
  ```bash
  python -m pip install --upgrade pip && pip install --no-cache-dir -r requirements_minimal.txt
  ```
- **Start Command**: 
  ```bash
  gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 300 app:app
  ```
- **Plan**: `Free`

### Step 4: Add Environment Variables
In the Render dashboard, add these environment variables:

```
SECRET_KEY=thisissecretkey
GEMINI_API_KEY=AIzaSyBEqJgbfk40_oU-G4nzCOW9vPwbE2cOc30
FLASK_ENV=production
FLASK_DEBUG=false
PYTHON_VERSION=3.11.9
RENDER=true
USE_MINIMAL_DEPS=true
```

### Step 5: Deploy!
- Click **"Create Web Service"**
- Render will automatically build and deploy your app
- Your app will be available at: `https://your-app-name.onrender.com`

## 🔧 What's Fixed

### ✅ **Python 3.11 Compatibility**
- Updated to Python 3.11.9 (stable with pandas)
- Fixed setuptools import issues
- Compatible pip version

### ✅ **Minimal Dependencies Option**
- Created `requirements_minimal.txt` without pandas
- Fallback CSV export using native Python
- Excel export with openpyxl only

### ✅ **Smart Import System**
- App automatically detects environment
- Uses minimal dependencies on Render
- Falls back gracefully if pandas unavailable

## 📊 After Deployment

### Check Your App
- **Application URL**: `https://ai-testcase-generator.onrender.com`
- **Health Check**: `https://ai-testcase-generator.onrender.com/health`

### Features Working
- ✅ **Document upload** (PDF, DOCX, TXT)
- ✅ **AI test case generation** with Gemini
- ✅ **Real-time progress** updates
- ✅ **CSV export** (native Python fallback)
- ✅ **Excel export** (openpyxl)
- ✅ **Statistics dashboard**

## 🎯 Alternative: Use render_minimal.yaml

If you prefer automatic configuration:

1. **Rename `render_minimal.yaml` to `render.yaml`**
2. **Push to GitHub**
3. **Render will use the YAML configuration automatically**

## 🔍 Troubleshooting

### If Build Still Fails
1. **Use minimal requirements**:
   ```bash
   # In Render dashboard, change build command to:
   pip install Flask==3.0.0 Flask-CORS==4.0.0 google-generativeai==0.3.2 python-dotenv==1.0.0 gunicorn==21.2.0
   ```

2. **Check Python version**:
   - Ensure Runtime is set to `Python 3.11.9`
   - Add `PYTHON_VERSION=3.11.9` environment variable

3. **Monitor build logs**:
   - Check real-time logs in Render dashboard
   - Look for specific error messages

---

**This fixed version should deploy successfully on Render! 🎉**
