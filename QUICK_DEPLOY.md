# 🚀 Quick Deployment Guide

## Prerequisites
1. **Get your Google Gemini API Key**:
   - Visit: https://makersuite.google.com/app/apikey
   - Create and copy your API key

## Option 1: Quick Local Deployment (Recommended for testing)

### Step 1: Setup Environment
```bash
# Copy environment template
copy .env.example .env

# Edit .env file and add your API key:
# GEMINI_API_KEY=your_actual_api_key_here
# SECRET_KEY=your_secure_secret_key_here
```

### Step 2: Install and Run
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### Step 3: Access Application
- Open browser: http://localhost:5000

## Option 2: Docker Deployment (Recommended for production)

### Prerequisites
- Install Docker Desktop for Windows

### Step 1: Setup Environment
```bash
copy .env.example .env
# Edit .env file with your actual values
```

### Step 2: Deploy with Docker Compose
```bash
# Run the deployment script
deploy.bat

# Or manually:
docker-compose up -d
```

### Step 3: Access Application
- Open browser: http://localhost:5000
- Health check: http://localhost:5000/health

## Option 3: Cloud Deployment

### Heroku (Free tier available)
1. **Install Heroku CLI**
2. **Deploy**:
   ```bash
   heroku login
   heroku create your-app-name
   heroku config:set GEMINI_API_KEY=your_api_key
   heroku config:set SECRET_KEY=your_secret_key
   git push heroku main
   ```

### Railway (Easy deployment)
1. **Connect GitHub repository to Railway**
2. **Set environment variables in dashboard**
3. **Deploy automatically**

### DigitalOcean App Platform
1. **Connect repository**
2. **Configure environment variables**
3. **Deploy with auto-scaling**

## Environment Variables Required

```env
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=your_secret_key_here
```

## Troubleshooting

### Common Issues
1. **"No API key found"** - Set GEMINI_API_KEY in .env file
2. **"Port already in use"** - Change port or stop conflicting service
3. **"Import errors"** - Run `pip install -r requirements.txt`

### Getting Help
- Check logs: `docker-compose logs -f`
- Health check: `curl http://localhost:5000/health`
- Stop application: `docker-compose down`

## Features
- 🤖 AI-powered test case generation from documents
- 📄 Support for PDF, DOCX, and TXT files
- 🔄 Real-time processing status
- 📊 Statistics and export to CSV/Excel
- 🎨 Modern web interface with drag-and-drop

---

**Need help?** Check the full DEPLOYMENT.md guide for detailed instructions.
