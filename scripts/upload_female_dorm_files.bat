@echo off
chcp 65001 >nul
echo ==================================
echo 上传女生宿舍数据文件到服务器
echo ==================================

set SERVER=root@8.134.32.47
set REMOTE_PATH=/root/workspace/DormBill/scripts/

echo.
echo 正在上传文件...
echo.

echo [1/3] 上传员工SQL...
scp scripts\import_female_dorm_employees.sql %SERVER%:%REMOTE_PATH%
if %errorlevel% neq 0 (
    echo ❌ 上传失败！
    pause
    exit /b 1
)

echo [2/3] 上传入住记录SQL...
scp scripts\import_female_dorm_records_fixed.sql %SERVER%:%REMOTE_PATH%
if %errorlevel% neq 0 (
    echo ❌ 上传失败！
    pause
    exit /b 1
)

echo [3/3] 上传执行脚本...
scp scripts\import_female_dorm_all.sh %SERVER%:%REMOTE_PATH%
if %errorlevel% neq 0 (
    echo ❌ 上传失败！
    pause
    exit /b 1
)

echo.
echo ==================================
echo ✅ 全部上传完成！
echo ==================================
echo.
echo 现在在服务器上执行：
echo cd /root/workspace/DormBill
echo bash scripts/import_female_dorm_all.sh
echo.
pause
