# PowerShell版本 - 导出本地数据库

$DB_NAME = "dorm_management"
$DB_USER = "root"
$TIMESTAMP = Get-Date -Format "yyyyMMdd_HHmmss"
$BACKUP_FILE = "dorm_backup_$TIMESTAMP.sql"
$MYSQL_PATH = "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe"

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "MySQL 数据库导出工具" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# 检查 mysqldump 是否存在
if (-not (Test-Path $MYSQL_PATH)) {
    Write-Host "❌ 找不到 mysqldump，请检查MySQL安装路径" -ForegroundColor Red
    Write-Host "当前查找路径: $MYSQL_PATH" -ForegroundColor Yellow
    exit 1
}

Write-Host "数据库: $DB_NAME" -ForegroundColor Green
Write-Host "用户: $DB_USER" -ForegroundColor Green
Write-Host "输出文件: $BACKUP_FILE" -ForegroundColor Green
Write-Host ""

# 提示输入密码
$Password = Read-Host "请输入MySQL密码" -AsSecureString
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($Password)
$PlainPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

Write-Host "开始导出..." -ForegroundColor Yellow

# 执行导出
& $MYSQL_PATH -u $DB_USER "-p$PlainPassword" --databases $DB_NAME --add-drop-database --default-character-set=utf8mb4 --result-file=$BACKUP_FILE 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ 导出成功！" -ForegroundColor Green
    Write-Host "文件: $BACKUP_FILE" -ForegroundColor Green
    $FileSize = (Get-Item $BACKUP_FILE).Length / 1KB
    Write-Host "大小: $([math]::Round($FileSize, 2)) KB" -ForegroundColor Green
    Write-Host ""
    Write-Host "下一步：将此文件上传到服务器" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "❌ 导出失败" -ForegroundColor Red
    exit 1
}

# 清理密码变量
[System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($BSTR)
$PlainPassword = $null
