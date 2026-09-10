@echo off
REM DormBill Docker 停止脚本 (Windows)
REM 双击此文件即可停止服务

echo ======================================
echo   DormBill Docker 停止脚本
echo ======================================
echo.

echo 正在停止服务 ...
docker-compose stop

echo.
echo ======================================
echo   服务已停止
echo ======================================
echo.
echo 如需再次启动，请双击 docker-start.bat
echo.
pause
