@echo off
echo ============================================
echo AI Shopping Assistant - Backend Setup
echo ============================================
echo.

echo [1/4] Creating virtual environment...
python -m venv venv

echo.
echo [2/4] Activating virtual environment...
call venv\Scripts\activate

echo.
echo [3/4] Upgrading pip, setuptools, and wheel...
python -m pip install --upgrade pip setuptools wheel

echo.
echo [4/4] Installing dependencies...
pip install --prefer-binary -r requirements.txt

echo.
echo ============================================
echo Setup complete!
echo ============================================
echo.
echo To run the backend server:
echo 1. Activate the virtual environment: venv\Scripts\activate
echo 2. Run the server: python app.py
echo.
pause
