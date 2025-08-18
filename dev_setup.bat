@echo off
setlocal enabledelayedexpansion

echo.
echo 🚀 AI Test Case Generator - Local Development Setup
echo.

:: Check if .env file exists
if not exist ".env" (
    echo [INFO] Creating .env file from template...
    copy .env.example .env > nul
    echo.
    echo [IMPORTANT] Please edit .env file and add your Google Gemini API key!
    echo 1. Open .env file in a text editor
    echo 2. Replace 'your-gemini-api-key-here' with your actual API key
    echo 3. Get your API key from: https://makersuite.google.com/app/apikey
    echo.
    echo Press any key after you've updated the .env file...
    pause > nul
)

:: Check if Python is installed
python --version > nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo [INFO] Python found, checking version...
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set python_version=%%i
echo [INFO] Python version: %python_version%

:: Check if virtual environment exists
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
)

:: Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

:: Install dependencies
echo [INFO] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

:: Create necessary directories
echo [INFO] Creating necessary directories...
if not exist "uploads" mkdir uploads
if not exist "downloads" mkdir downloads

:: Check if GEMINI_API_KEY is set
for /f "tokens=2 delims==" %%i in ('findstr "GEMINI_API_KEY" .env 2^>nul') do set api_key=%%i
if "%api_key%"=="your-gemini-api-key-here" (
    echo.
    echo [WARNING] GEMINI_API_KEY is not configured!
    echo Please edit .env file and set your actual API key.
    echo.
    echo Press any key to continue anyway...
    pause > nul
)

:: Start the application
echo.
echo [INFO] Starting the application...
echo.
echo 📋 Application Information:
echo ========================
echo URL: http://localhost:5000
echo Environment: Development
echo Debug Mode: Enabled
echo.
echo 🔧 Controls:
echo Ctrl+C to stop the application
echo.
echo Opening browser...
timeout /t 3 /nobreak > nul
start http://localhost:5000

:: Run the application
python app.py

echo.
echo [INFO] Application stopped.
echo Press any key to exit...
pause > nul
