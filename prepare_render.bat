@echo off
echo.
echo 🚀 Preparing for Render Deployment...
echo.

:: Check if git is available
git --version > nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git is not installed. Please install Git first.
    pause
    exit /b 1
)

:: Check if we're in a git repository
if not exist ".git" (
    echo [INFO] Initializing git repository...
    git init
    git remote add origin https://github.com/patilmanas915/TestCaseGenerator.git
)

:: Add all files
echo [INFO] Adding files to git...
git add .

:: Commit changes
echo [INFO] Committing changes...
git commit -m "Fix Render deployment - Python 3.11 + minimal dependencies"

:: Push to GitHub
echo [INFO] Pushing to GitHub...
git push -u origin main

if errorlevel 1 (
    echo [WARNING] Push failed. You may need to resolve conflicts.
    echo Please check your GitHub repository and try again.
    pause
    exit /b 1
)

echo.
echo ✅ Code pushed to GitHub successfully!
echo.
echo 📋 Next Steps for Render Deployment:
echo =====================================
echo 1. Go to https://render.com and sign up
echo 2. Click "New +" then "Web Service"
echo 3. Connect your GitHub repository: TestCaseGenerator
echo 4. Use these UPDATED settings:
echo    - Runtime: Python 3.11.9
echo    - Build Command: python -m pip install --upgrade pip ^&^& pip install --no-cache-dir -r requirements_minimal.txt
echo    - Start Command: gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 300 app:app
echo 5. Add environment variables:
echo    - SECRET_KEY=thisissecretkey
echo    - GEMINI_API_KEY=AIzaSyBEqJgbfk40_oU-G4nzCOW9vPwbE2cOc30
echo    - FLASK_ENV=production
echo    - PYTHON_VERSION=3.11.9
echo    - RENDER=true
echo    - USE_MINIMAL_DEPS=true
echo 6. Click "Create Web Service"
echo.
echo 🌐 Your app will be available at: https://your-app-name.onrender.com
echo.
echo Press any key to exit...
pause > nul
