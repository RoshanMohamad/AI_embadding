@echo off
echo ============================================
echo Starting AI Shopping Assistant Frontend
echo ============================================
echo.

if not exist node_modules (
    echo ERROR: Dependencies not installed!
    echo Please run setup.bat first.
    pause
    exit /b 1
)

echo Starting Next.js development server...
echo Frontend will be available at http://localhost:3000
echo.
echo Press Ctrl+C to stop the server
echo.

call npm run dev
