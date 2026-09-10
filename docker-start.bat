@echo off
REM DormBill Docker 快速启动脚本 (Windows)
REM 双击此文件即可启动服务

echo ======================================
echo   DormBill Docker 启动脚本
echo ======================================
echo.

REM 检查 Docker 是否安装
docker --version >nul 2>&1
if errorlevel 1 (
    echo [错误] Docker 未安装或未启动
    echo 请先安装并启动 Docker Desktop
    echo 下载地址: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo [1/4] 检查 Docker ... 已安装

REM 检查环境变量文件
if not exist .env (
    echo [2/4] 创建 .env 文件 ...
    copy .env.docker .env
    echo.
    echo [重要] 请编辑 .env 文件修改数据库密码！
    echo 按任意键继续...
    pause >nul
) else (
    echo [2/4] 检查 .env 文件 ... 已存在
)

REM 启动服务
echo [3/4] 启动 Docker 服务 ...
docker-compose up -d

REM 等待服务启动
echo [4/4] 等待服务启动 ...
timeout /t 10 /nobreak >nul

REM 显示状态
echo.
echo ======================================
echo   服务启动完成！
echo ======================================
docker-compose ps
echo.
echo 访问地址:
echo   前端: http://localhost
echo   后端 API: http://localhost:8000/docs
echo.
echo 常用命令:
echo   查看日志: docker-compose logs -f
echo   停止服务: docker-compose stop
echo   重启服务: docker-compose restart
echo.
pause
