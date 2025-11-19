@echo off
REM ============================================================
REM SMART HOUSE - AUTO-START EVERYTHING
REM ============================================================
title Smart House

cls
echo.
echo ============================================================
echo            SMART HOUSE - STARTING...
echo ============================================================
echo.

cd /d "%~dp0"

REM Start web app minimized
echo [1/2] Starting web dashboard...
start "Web Dashboard" /MIN cmd /c "cd web-app && npm run dev"

timeout /t 2 /nobreak >nul

REM Start bridge
echo [2/2] Starting bridge...
echo.
echo ============================================================
echo SYSTEM RUNNING!
echo ============================================================
echo.
echo Web Dashboard: http://localhost:3000
echo Bridge monitoring below (keep this window open!)
echo.
echo Press Ctrl+C to stop
echo ============================================================
echo.

python unified_bridge.py

echo.
echo ============================================================
echo Bridge stopped.
echo ============================================================
pause
