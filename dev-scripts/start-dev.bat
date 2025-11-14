@echo off
echo ============================================================
echo 🚀 UFC PREDICTION SYSTEM - DEVELOPMENT MODE
echo ============================================================
echo.

cd /d "%~dp0\.."

echo 📊 Starting Developer Dashboard...
start "Dev Dashboard" cmd /k "cd dev-dashboard && ..\.venv\Scripts\python.exe app.py"

timeout /t 2 /nobreak >nul

echo 🔧 Starting Backend Server...
start "Backend API" cmd /k "cd backend && ..\.venv\Scripts\python.exe app.py"

timeout /t 3 /nobreak >nul

echo 🎯 Starting Frontend Server...
start "Frontend App" cmd /k "cd frontend && npm run dev"

echo.
echo ============================================================
echo 🎉 DEVELOPMENT SERVERS STARTING...
echo ============================================================
echo 📊 Developer Dashboard: http://localhost:5001
echo 🔧 Backend API:         http://localhost:8000
echo 🎯 Frontend App:        http://localhost:3000
echo ============================================================
echo.
echo ✅ All services are starting up...
echo ✅ Check the Developer Dashboard for real-time status!
echo.
pause
echo.
echo Press any key to stop all services...
pause >nul

echo Stopping services...
taskkill /F /IM node.exe /T >nul 2>&1
taskkill /F /IM python.exe /T >nul 2>&1
echo All services stopped.
pause