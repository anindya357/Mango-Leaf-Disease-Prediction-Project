@echo off
REM Mango Leaf Disease Prediction - Quick Start Script (Windows)
REM This script sets up and runs both backend and frontend

title Mango Leaf Disease Prediction System
color 0A

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║    🥭 Mango Leaf Disease Prediction System 🥭             ║
echo ║              Quick Start - Windows                         ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    echo Make sure to check 'Add Python to PATH' during installation
    pause
    exit /b 1
)

echo [✓] Python found
echo.

REM Check if git is available (optional)
git --version >nul 2>&1
if errorlevel 1 (
    echo [!] Git not found (optional, for version control)
)

echo.
echo ═══════════════════════════════════════════════════════════
echo STEP 1: Setting up Backend
echo ═══════════════════════════════════════════════════════════
echo.

cd backend

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [✓] Virtual environment created
) else (
    echo [✓] Virtual environment already exists
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)
echo [✓] Virtual environment activated

echo.
echo Installing backend dependencies...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [✓] Dependencies installed

echo.
echo ═══════════════════════════════════════════════════════════
echo STEP 2: Verifying Model File
echo ═══════════════════════════════════════════════════════════
echo.

if not exist "models\mango_leaf_disease_MobileNetV2_model.h5" (
    echo.
    echo [!] Model file not found at: models\mango_leaf_disease_MobileNetV2_model.h5
    echo.
    echo You need to train the model first:
    echo 1. Open notebooks\train_model.ipynb in Jupyter
    echo 2. Run all cells in the notebook
    echo 3. The model will be saved to backend\models\
    echo.
    echo For now, we'll start the backend anyway.
    echo The API will fail on predictions until the model exists.
) else (
    echo [✓] Model file found: models\mango_leaf_disease_MobileNetV2_model.h5
)

echo.
echo ═══════════════════════════════════════════════════════════
echo STEP 3: Starting Backend Server
echo ═══════════════════════════════════════════════════════════
echo.
echo Backend will start at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo Press CTRL+C to stop the server
echo.

timeout /t 2

python main.py

REM This will keep the window open if there's an error
if errorlevel 1 (
    echo.
    echo [ERROR] Backend failed to start
    echo.
    pause
)
