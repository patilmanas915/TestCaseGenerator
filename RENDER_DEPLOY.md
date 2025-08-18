# 🚀 Render Deployment Guide for AI Test Case Generator

## Quick Deploy to Render (Free)

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Add Render deployment configuration"
git push origin main
```

### Step 2: Deploy on Render
1. **Go to [render.com](https://render.com) and sign up**
2. **Click "New +" → "Web Service"**
3. **Connect your GitHub repository: `TestCaseGenerator`**

### Step 3: Configure Deployment
**Service Configuration:**
- **Name**: `ai-testcase-generator`
- **Environment**: `Python 3`
- **Build Command**: 
  ```bash
  pip install --upgrade pip setuptools wheel && pip install --no-cache-dir -r requirements.txt
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
PYTHON_VERSION=3.9.16
RENDER=true
```

### Step 5: Deploy!
- Click **"Create Web Service"**
- Render will automatically build and deploy your app
- Your app will be available at: `https://your-app-name.onrender.com`

## 🔧 Alternative: Manual Configuration

If you prefer to use the `render.yaml` file:

1. **Use the provided `render.yaml` configuration**
2. **Render will automatically detect and use it**
3. **Just add environment variables in the dashboard**

## 📊 After Deployment

### Check Your App
- **Application URL**: `https://ai-testcase-generator.onrender.com`
- **Health Check**: `https://ai-testcase-generator.onrender.com/health`

### Monitor Deployment
- **View Logs**: In Render dashboard → Logs
- **Check Status**: Dashboard shows build and deployment status
- **Auto-deploys**: Every GitHub push triggers automatic deployment

## 🎯 Features Enabled
- ✅ **Free hosting** (512MB RAM, 100GB bandwidth)
- ✅ **Automatic HTTPS** certificate
- ✅ **Auto-deploys** from GitHub
- ✅ **Health monitoring** with `/health` endpoint
- ✅ **Gemini AI integration** ready
- ✅ **File upload/download** functionality
- ✅ **Optimized for pandas** (no compilation issues)

## 🔍 Troubleshooting

### Common Issues
1. **Build fails**: Check logs in Render dashboard
2. **Environment variables**: Ensure all required vars are set
3. **Health check fails**: Verify `/health` endpoint works
4. **Timeout errors**: Increase worker timeout if needed

### Getting Help
- **Render Logs**: Real-time build and runtime logs
- **Health Check**: Built-in monitoring
- **GitHub Integration**: Automatic deployments

---

**Your AI Test Case Generator is now ready for free deployment on Render! 🎉**
