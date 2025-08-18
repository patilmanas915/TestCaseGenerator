@echo off
setlocal enabledelayedexpansion

:: Production Deployment Script for AI Test Case Generator (Windows)
:: This script sets up and deploys the application in production mode

echo.
echo 🚀 Starting AI Test Case Generator Deployment...
echo.

:: Check if .env file exists
if not exist ".env" (
    echo [WARNING] .env file not found. Creating from template...
    copy .env.example .env > nul
    echo [ERROR] Please edit .env file with your actual values before continuing!
    pause
    exit /b 1
)

:: Check if Docker is installed
docker --version > nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

:: Check if Docker Compose is installed
docker-compose --version > nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

echo [INFO] Environment checks passed successfully

:: Create necessary directories
echo [INFO] Creating necessary directories...
if not exist "uploads" mkdir uploads
if not exist "downloads" mkdir downloads
if not exist "logs" mkdir logs

:: Build Docker image
echo [INFO] Building Docker image...
docker build -t ai-testcase-generator:latest .
if errorlevel 1 (
    echo [ERROR] Failed to build Docker image
    pause
    exit /b 1
)

:: Stop existing containers
echo [INFO] Stopping existing containers...
docker-compose down 2>nul

:: Start services
echo [INFO] Starting services with Docker Compose...
docker-compose up -d
if errorlevel 1 (
    echo [ERROR] Failed to start services
    pause
    exit /b 1
)

:: Wait for services to be ready
echo [INFO] Waiting for services to start...
timeout /t 10 /nobreak > nul

:: Check if application is healthy
echo [INFO] Checking application health...
set max_attempts=30
set attempt=1

:health_check_loop
curl -f http://localhost:5000/health > nul 2>&1
if !errorlevel! equ 0 (
    echo [INFO] ✅ Application is healthy and ready!
    goto :deployment_success
) else (
    if !attempt! geq !max_attempts! (
        echo [ERROR] ❌ Application failed to start properly
        docker-compose logs
        pause
        exit /b 1
    )
    echo [INFO] Attempt !attempt!/!max_attempts! - waiting for application...
    timeout /t 5 /nobreak > nul
    set /a attempt+=1
    goto :health_check_loop
)

:deployment_success
:: Display deployment information
echo.
echo 🎉 Deployment completed successfully!
echo.
echo 📋 Deployment Information:
echo ==========================
echo Application URL: http://localhost:5000
echo Health Check: http://localhost:5000/health
echo Environment: Production
echo Workers: 4
echo.
echo 📊 Container Status:
docker-compose ps
echo.
echo 📝 Useful Commands:
echo View logs: docker-compose logs -f
echo Stop application: docker-compose down
echo Restart application: docker-compose restart
echo Update application: docker-compose up -d --build
echo.
echo 🔧 Monitoring:
echo Check health: curl http://localhost:5000/health
echo View metrics: docker stats
echo.

:: Optional: Open browser
echo Opening application in browser...
start http://localhost:5000

echo [INFO] Deployment script completed!
echo Press any key to exit...
pause > nul
