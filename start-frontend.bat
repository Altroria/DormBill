@echo off
chcp 65001 >nul
echo ========================================
echo   蓉蓉的收租小工具 - 前端服务启动
echo ========================================
echo.

cd /d "%~dp0frontend"

echo [1/3] 检查 Node.js 环境...
node --version
if errorlevel 1 (
    echo [错误] 未检测到 Node.js，请先安装 Node.js 16+
    pause
    exit /b 1
)

echo.
echo [2/3] 检查依赖...
if not exist "node_modules" (
    echo [提示] 检测到依赖未安装，开始安装...
    npm install
)

echo.
echo [3/3] 启动前端服务...
echo [提示] 访问地址: http://localhost:5173
echo [提示] 按 Ctrl+C 停止服务
echo.
npm run dev

pause
