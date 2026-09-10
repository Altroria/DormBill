# 
# DormBill 部署脚本 (Windows PowerShell)
# 
# 使用方法:
#   .\scripts\deploy.ps1 dev     # 开发环境部署
#   .\scripts\deploy.ps1 prod    # 生产环境部署
#   .\scripts\deploy.ps1 stop    # 停止服务
#   .\scripts\deploy.ps1 restart # 重启服务
#   .\scripts\deploy.ps1 logs    # 查看日志
#

param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

$ErrorActionPreference = "Stop"
$ProjectDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $ProjectDir

# 日志函数
function Log-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Green
}

function Log-Warn {
    param([string]$Message)
    Write-Host "[WARN] $Message" -ForegroundColor Yellow
}

function Log-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# 检查 Docker 是否安装
function Check-Docker {
    try {
        $null = docker --version
        $null = docker-compose --version
    } catch {
        Log-Error "Docker 或 Docker Compose 未安装，请先安装 Docker Desktop"
        exit 1
    }
}

# 检查环境变量文件
function Check-Env {
    if (-not (Test-Path ".env")) {
        Log-Warn ".env 文件不存在，从 .env.docker 复制"
        Copy-Item ".env.docker" ".env"
        Log-Info "已创建 .env 文件，请根据实际情况修改配置"
        Read-Host "按 Enter 键继续"
    }
}

# 开发环境部署
function Deploy-Dev {
    Log-Info "开始部署开发环境..."
    Check-Docker
    Check-Env

    Log-Info "构建并启动服务..."
    docker-compose up -d --build

    Log-Info "等待服务启动..."
    Start-Sleep -Seconds 10

    Log-Info "检查服务状态..."
    docker-compose ps

    Write-Host ""
    Log-Info "=========================================="
    Log-Info "开发环境部署完成！"
    Log-Info "=========================================="
    Log-Info "前端访问: http://localhost"
    Log-Info "后端 API: http://localhost:8000/docs"
    Log-Info "健康检查: http://localhost:8000/health"
    Log-Info "=========================================="
    Write-Host ""
    Log-Info "查看日志: docker-compose logs -f"
}

# 生产环境部署
function Deploy-Prod {
    Log-Info "开始部署生产环境..."
    Check-Docker
    Check-Env

    # 检查必需的环境变量
    $envContent = Get-Content ".env" -Raw
    if ($envContent -match "DB_PASSWORD=dormbill123") {
        Log-Error "请修改 .env 中的 DB_PASSWORD 为强密码！"
        exit 1
    }

    if (Test-Path ".git") {
        Log-Info "拉取最新代码..."
        git pull
    }

    Log-Info "构建并启动服务（生产配置）..."
    docker-compose -f docker-compose.prod.yml up -d --build

    Log-Info "等待服务启动..."
    Start-Sleep -Seconds 15

    Log-Info "检查服务状态..."
    docker-compose -f docker-compose.prod.yml ps

    Write-Host ""
    Log-Info "=========================================="
    Log-Info "生产环境部署完成！"
    Log-Info "=========================================="
    Log-Info "前端访问: http://localhost"
    Log-Info "=========================================="
    Write-Host ""
    Log-Info "查看日志: docker-compose -f docker-compose.prod.yml logs -f"
}

# 停止服务
function Stop-Services {
    Log-Info "停止服务..."
    
    $devRunning = docker-compose ps 2>$null | Select-String "Up"
    if ($devRunning) {
        docker-compose stop
        Log-Info "开发环境已停止"
    }

    $prodRunning = docker-compose -f docker-compose.prod.yml ps 2>$null | Select-String "Up"
    if ($prodRunning) {
        docker-compose -f docker-compose.prod.yml stop
        Log-Info "生产环境已停止"
    }

    Log-Info "服务已停止"
}

# 重启服务
function Restart-Services {
    Log-Info "重启服务..."
    
    $devRunning = docker-compose ps 2>$null | Select-String "dormbill"
    if ($devRunning) {
        docker-compose restart
        Log-Info "开发环境已重启"
        return
    }

    $prodRunning = docker-compose -f docker-compose.prod.yml ps 2>$null | Select-String "dormbill"
    if ($prodRunning) {
        docker-compose -f docker-compose.prod.yml restart
        Log-Info "生产环境已重启"
        return
    }

    Log-Error "未找到运行中的服务"
    exit 1
}

# 查看日志
function View-Logs {
    $devRunning = docker-compose ps 2>$null | Select-String "dormbill"
    if ($devRunning) {
        docker-compose logs -f --tail=100
        return
    }

    $prodRunning = docker-compose -f docker-compose.prod.yml ps 2>$null | Select-String "dormbill"
    if ($prodRunning) {
        docker-compose -f docker-compose.prod.yml logs -f --tail=100
        return
    }

    Log-Error "未找到运行中的服务"
    exit 1
}

# 备份数据库
function Backup-Database {
    Log-Info "开始备份数据库..."
    
    $BackupDir = "backups"
    if (-not (Test-Path $BackupDir)) {
        New-Item -ItemType Directory -Path $BackupDir | Out-Null
    }
    
    $BackupFile = "$BackupDir\dormbill_$(Get-Date -Format 'yyyyMMdd_HHmmss').sql"
    
    # 读取环境变量
    Get-Content ".env" | ForEach-Object {
        if ($_ -match '^([^=]+)=(.*)$') {
            Set-Variable -Name $matches[1] -Value $matches[2] -Scope Script
        }
    }
    
    $devRunning = docker-compose ps 2>$null | Select-String "dormbill-mysql"
    $prodRunning = docker-compose -f docker-compose.prod.yml ps 2>$null | Select-String "dormbill-mysql"
    
    if ($devRunning) {
        docker-compose exec -T mysql mysqldump -uroot -p"$DB_PASSWORD" dormbill | Out-File -FilePath $BackupFile -Encoding utf8
    } elseif ($prodRunning) {
        docker-compose -f docker-compose.prod.yml exec -T mysql mysqldump -uroot -p"$DB_PASSWORD" dormbill | Out-File -FilePath $BackupFile -Encoding utf8
    } else {
        Log-Error "MySQL 容器未运行"
        exit 1
    }
    
    Log-Info "数据库备份完成: $BackupFile"
}

# 显示帮助信息
function Show-Help {
    Write-Host "DormBill 部署脚本"
    Write-Host ""
    Write-Host "使用方法:"
    Write-Host "  .\scripts\deploy.ps1 <command>"
    Write-Host ""
    Write-Host "可用命令:"
    Write-Host "  dev      - 部署开发环境"
    Write-Host "  prod     - 部署生产环境"
    Write-Host "  stop     - 停止服务"
    Write-Host "  restart  - 重启服务"
    Write-Host "  logs     - 查看日志"
    Write-Host "  backup   - 备份数据库"
    Write-Host "  help     - 显示此帮助信息"
}

# 主逻辑
switch ($Command) {
    "dev" {
        Deploy-Dev
    }
    "prod" {
        Deploy-Prod
    }
    "stop" {
        Stop-Services
    }
    "restart" {
        Restart-Services
    }
    "logs" {
        View-Logs
    }
    "backup" {
        Backup-Database
    }
    "help" {
        Show-Help
    }
    default {
        Log-Error "未知命令: $Command"
        Show-Help
        exit 1
    }
}
