@echo off
chcp 65001 >nul
echo ========================================
echo   蓉蓉的收租小工具 - 后端服务启动
echo ========================================
echo.

cd /d "%~dp0backend"

echo [1/3] 检查 Python 环境...
python --version
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python 3.10+
    pause
    exit /b 1
)

echo.
echo [2/3] 检查依赖...
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo [提示] 检测到依赖未安装，开始安装...
    pip install -r requirements.txt
)

echo.
echo [3/3] 启动后端服务...
echo [提示] API 文档: http://localhost:8000/docs
echo [提示] 按 Ctrl+C 停止服务
echo.
python run.py

pause
