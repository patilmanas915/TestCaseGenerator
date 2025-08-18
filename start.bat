@echo off
echo Starting AI Test Case Generator Web Application...
echo.

:: Check if virtual environment exists and activate it
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo No virtual environment found, using system Python...
)

:: Start the application
echo.
echo Starting Flask application...
echo Open your browser and go to: http://localhost:5000
echo.
python app.py
echo.
echo Application has stopped. Press any key to close this window...
pause >nul
