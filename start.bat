@echo off
chcp 65001 >nul
title RAG QA System - 启动管理

:menu
cls
echo ============================================
echo    RAG QA System - AI 技术文档智能问答系统
echo ============================================
echo.
echo    [1] 启动后端 (FastAPI :8000)
echo    [2] 启动前端 (Vite   :5173)
echo    [3] 同时启动前后端
echo    [4] 安装后端依赖
echo    [5] 安装前端依赖
echo    [6] 重建向量索引
echo    [0] 退出
echo.
set /p choice="请输入选项: "

if "%choice%"=="1" goto start_backend
if "%choice%"=="2" goto start_frontend
if "%choice%"=="3" goto start_both
if "%choice%"=="4" goto install_backend
if "%choice%"=="5" goto install_frontend
if "%choice%"=="6" goto rebuild_index
if "%choice%"=="0" goto exit
goto menu

:start_backend
cls
echo [启动后端] FastAPI 服务...
echo.
cd /d "%~dp0backend"

REM 检查 .env 是否存在
if not exist ".env" (
    echo [警告] 未找到 .env 文件！
    echo 请复制 .env.example 为 .env 并填入 DeepSeek API Key
    echo.
    pause
    goto menu
)

echo 后端地址: http://localhost:8000
echo API 文档: http://localhost:8000/docs
echo.
echo 关闭此窗口可停止后端服务
echo ============================================
start "RAG-Backend" cmd /k "cd /d %~dp0backend && python main.py"
goto menu

:start_frontend
cls
echo [启动前端] Vite 开发服务器...
echo.
cd /d "%~dp0frontend"

REM 检查 node_modules 是否存在
if not exist "node_modules\" (
    echo [提示] 尚未安装依赖，正在自动安装...
    call npm install
)

echo 前端地址: http://localhost:5173
echo.
echo 关闭此窗口可停止前端服务
echo ============================================
start "RAG-Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"
goto menu

:start_both
cls
echo [同时启动] 前后端服务...
echo.

REM 后端
cd /d "%~dp0backend"
if not exist ".env" (
    echo [警告] 未找到 .env 文件，后端可能无法正常工作！
)
start "RAG-Backend" cmd /k "cd /d %~dp0backend && python main.py"
echo [OK] 后端已在新窗口启动 → http://localhost:8000

REM 前端
cd /d "%~dp0frontend"
if not exist "node_modules\" (
    echo [提示] 正在安装前端依赖...
    call npm install
)
start "RAG-Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"
echo [OK] 前端已在新窗口启动 → http://localhost:5173

echo.
echo 两个服务分别在独立的命令行窗口中运行。
echo 关闭对应窗口即可停止服务。
echo.
pause
goto menu

:install_backend
cls
echo [安装] 后端 Python 依赖...
echo.
cd /d "%~dp0backend"
pip install -r requirements.txt
echo.
echo [完成] 后端依赖安装完毕
echo.
pause
goto menu

:install_frontend
cls
echo [安装] 前端 Node.js 依赖...
echo.
cd /d "%~dp0frontend"
call npm install
echo.
echo [完成] 前端依赖安装完毕
echo.
pause
goto menu

:rebuild_index
cls
echo [重建] Chroma 向量索引...
echo.
cd /d "%~dp0backend"
python -c "from vector_store import get_vector_store; from config import DOCUMENTS_PATH; s=get_vector_store(); c=s.rebuild_from_directory(DOCUMENTS_PATH); print(f'索引重建完成: {c} 个片段')"
echo.
pause
goto menu

:exit
exit
