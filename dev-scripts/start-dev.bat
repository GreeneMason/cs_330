@echo off
echo Starting UFC Prediction System Development Environment...
echo.

echo [1/3] Setting up Python backend...
cd backend
call ..\.venv\Scripts\activate
echo Backend Python environment activated

echo.
echo [2/3] Starting frontend development server...
cd ..\frontend
start "Frontend Dev Server" cmd /c "npm run dev"

echo.
echo [3/3] Starting backend API server...
cd ..\backend
start "Backend API Server" cmd /c "python app.py"

echo.
echo =================================
echo Development Environment Started!
echo =================================
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:8000
echo.
echo Press any key to stop all services...
pause >nul

echo Stopping services...
taskkill /F /IM node.exe /T >nul 2>&1
taskkill /F /IM python.exe /T >nul 2>&1
echo All services stopped.
pause