@echo off
echo ============================================
echo AI Shopping Assistant - Backend Setup
echo ============================================
echo.

echo [1/3] Creating virtual environment...
python -m venv venv

echo.
echo [2/3] Activating virtual environment...
call venv\Scripts\activate

echo.
echo [3/3] Installing dependencies...
pip install -r requirements.txt

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
