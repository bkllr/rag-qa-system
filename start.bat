@echo off
title RAG QA System

:menu
cls
echo ============================================
echo    RAG QA System - AI Doc Q&A
echo ============================================
echo.
echo    [1] Start Backend  (FastAPI :8000)
echo    [2] Start Frontend (Vite   :5173)
echo    [3] Start Both
echo    [4] Install Backend Deps
echo    [5] Install Frontend Deps
echo    [6] Rebuild Vector Index
echo    [7] Restart Both Services
echo    [0] Exit
echo.
set /p choice=Select option: 

if "%choice%"=="1" goto start_backend
if "%choice%"=="2" goto start_frontend
if "%choice%"=="3" goto start_both
if "%choice%"=="4" goto install_backend
if "%choice%"=="5" goto install_frontend
if "%choice%"=="6" goto rebuild_index
if "%choice%"=="7" goto restart_both
if "%choice%"=="0" goto exit
goto menu

:start_backend
cls
echo === Starting Backend ===
cd /d "%~dp0backend"
if not exist ".env" (
    echo [WARNING] .env file not found!
    echo Please copy .env.example to .env and set your DeepSeek API Key.
    echo.
    pause
    goto menu
)
echo Backend  : http://localhost:8000
echo API Docs : http://localhost:8000/docs
echo Close this window to stop the backend.
echo.
start "RAG-Backend" /d "%~dp0backend" cmd /k python main.py
goto menu

:start_frontend
cls
echo === Starting Frontend ===
cd /d "%~dp0frontend"
if not exist "node_modules\" (
    echo Dependencies not installed. Installing...
    call npm install
)
echo Frontend : http://localhost:5173
echo Close this window to stop the frontend.
echo.
start "RAG-Frontend" /d "%~dp0frontend" cmd /k npm run dev
goto menu

:start_both
cls
echo === Starting Both Services ===
cd /d "%~dp0backend"
if not exist ".env" ( echo [WARNING] .env not found! Backend may fail. )
start "RAG-Backend" /d "%~dp0backend" cmd /k python main.py
echo [OK] Backend  -^> http://localhost:8000
cd /d "%~dp0frontend"
if not exist "node_modules\" ( call npm install )
start "RAG-Frontend" /d "%~dp0frontend" cmd /k npm run dev
echo [OK] Frontend -^> http://localhost:5173
echo.
echo Both services started in separate windows.
echo Close each window to stop the corresponding service.
echo.
pause
goto menu

:install_backend
cls
echo === Installing Backend Dependencies ===
cd /d "%~dp0backend"
pip install -r requirements.txt
echo.
echo Done.
pause
goto menu

:install_frontend
cls
echo === Installing Frontend Dependencies ===
cd /d "%~dp0frontend"
call npm install
echo.
echo Done.
pause
goto menu

:rebuild_index
cls
echo === Rebuilding Vector Index ===
cd /d "%~dp0backend"
python -c "from vector_store import get_vector_store; from config import DOCUMENTS_PATH; s=get_vector_store(); c=s.rebuild_from_directory(DOCUMENTS_PATH); print(f'Rebuilt: {c} chunks')"
echo.
pause
goto menu

:restart_both
cls
echo === Restarting Both Services ===
echo Killing processes on ports 8000 and 5173...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000.*LISTENING"') do taskkill /PID %%a /F 2^>nul
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5173.*LISTENING"') do taskkill /PID %%a /F 2^>nul
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5174.*LISTENING"') do taskkill /PID %%a /F 2^>nul
timeout /t 2 /nobreak ^>nul
goto start_both

:exit
exit
