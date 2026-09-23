@echo off
REM Windows版本 - 导出本地数据库

set DB_NAME=dorm_management
set DB_USER=root
set BACKUP_FILE=dorm_backup_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%.sql
set BACKUP_FILE=%BACKUP_FILE: =0%

echo 开始导出数据库 %DB_NAME%...
mysqldump -u %DB_USER% -p %DB_NAME% > %BACKUP_FILE%

if %ERRORLEVEL% EQU 0 (
    echo ✅ 导出成功: %BACKUP_FILE%
    dir %BACKUP_FILE%
) else (
    echo ❌ 导出失败
    exit /b 1
)

pause
