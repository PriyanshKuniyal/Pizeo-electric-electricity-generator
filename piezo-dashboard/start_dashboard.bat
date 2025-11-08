@echo off
echo Starting Piezoelectric Energy Dashboard...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

REM Navigate to the dashboard directory
cd /d "%~dp0"

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Start the server
echo.
echo ========================================
echo   Piezoelectric Dashboard Starting!
echo ========================================
echo.
echo Dashboard will be available at:
echo   http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.

cd backend
python main.py

pause
