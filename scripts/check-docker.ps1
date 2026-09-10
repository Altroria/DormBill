#
# DormBill Docker 环境检查脚本 (Windows PowerShell)
# 使用方法: .\scripts\check-docker.ps1
#

$ErrorActionPreference = "Continue"

Write-Host "======================================" -ForegroundColor Blue
Write-Host "  DormBill Docker 环境检查" -ForegroundColor Blue
Write-Host "======================================" -ForegroundColor Blue
Write-Host ""

# 检查项计数
$TotalChecks = 0
$PassedChecks = 0
$FailedChecks = 0

# 检查函数
function Check-Item {
    param(
        [string]$Name,
        [scriptblock]$Command
    )
    
    $script:TotalChecks++
    Write-Host "检查 $Name ... " -NoNewline
    
    try {
        $null = & $Command
        Write-Host "✓ 通过" -ForegroundColor Green
        $script:PassedChecks++
        return $true
    } catch {
        Write-Host "✗ 失败" -ForegroundColor Red
        $script:FailedChecks++
        return $false
    }
}

# 1. 检查 Docker
Write-Host "[1/8] 检查 Docker 安装" -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "检查 Docker ... ✓ 通过" -ForegroundColor Green
    Write-Host "  版本: $dockerVersion"
    $TotalChecks++
    $PassedChecks++
} catch {
    Write-Host "检查 Docker ... ✗ 失败" -ForegroundColor Red
    Write-Host "  请安装 Docker Desktop: https://www.docker.com/products/docker-desktop" -ForegroundColor Red
    $TotalChecks++
    $FailedChecks++
}
Write-Host ""

# 2. 检查 Docker Compose
Write-Host "[2/8] 检查 Docker Compose" -ForegroundColor Yellow
try {
    $composeVersion = docker-compose --version
    Write-Host "检查 Docker Compose ... ✓ 通过" -ForegroundColor Green
    Write-Host "  版本: $composeVersion"
    $TotalChecks++
    $PassedChecks++
} catch {
    Write-Host "检查 Docker Compose ... ✗ 失败" -ForegroundColor Red
    Write-Host "  请安装 Docker Compose" -ForegroundColor Red
    $TotalChecks++
    $FailedChecks++
}
Write-Host ""

# 3. 检查 Docker 服务状态
Write-Host "[3/8] 检查 Docker 服务" -ForegroundColor Yellow
try {
    $null = docker info 2>$null
    Write-Host "检查 Docker 守护进程 ... ✓ 通过" -ForegroundColor Green
    Write-Host "  Docker 服务正在运行" -ForegroundColor Green
    $TotalChecks++
    $PassedChecks++
} catch {
    Write-Host "检查 Docker 守护进程 ... ✗ 失败" -ForegroundColor Red
    Write-Host "  Docker 服务未启动，请启动 Docker Desktop" -ForegroundColor Red
    $TotalChecks++
    $FailedChecks++
}
Write-Host ""

# 4. 检查端口占用
Write-Host "[4/8] 检查端口占用" -ForegroundColor Yellow

function Test-Port {
    param([int]$Port)
    $connections = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
    return $null -eq $connections
}

# 端口 80
$TotalChecks++
if (Test-Port -Port 80) {
    Write-Host "检查 端口 80 (前端) ... ✓ 通过" -ForegroundColor Green
    Write-Host "  端口 80 可用" -ForegroundColor Green
    $PassedChecks++
} else {
    Write-Host "检查 端口 80 (前端) ... ✗ 失败" -ForegroundColor Red
    Write-Host "  端口 80 已被占用" -ForegroundColor Red
    Write-Host "  运行以下命令查看占用进程:" -ForegroundColor Yellow
    Write-Host "    netstat -ano | findstr :80" -ForegroundColor Yellow
    $FailedChecks++
}

# 端口 8000
$TotalChecks++
if (Test-Port -Port 8000) {
    Write-Host "检查 端口 8000 (后端) ... ✓ 通过" -ForegroundColor Green
    Write-Host "  端口 8000 可用" -ForegroundColor Green
    $PassedChecks++
} else {
    Write-Host "检查 端口 8000 (后端) ... ⚠ 警告" -ForegroundColor Yellow
    Write-Host "  端口 8000 已被占用（可选端口，不影响使用）" -ForegroundColor Yellow
    $PassedChecks++
}

# 端口 3306
$TotalChecks++
if (Test-Port -Port 3306) {
    Write-Host "检查 端口 3306 (MySQL) ... ✓ 通过" -ForegroundColor Green
    Write-Host "  端口 3306 可用" -ForegroundColor Green
    $PassedChecks++
} else {
    Write-Host "检查 端口 3306 (MySQL) ... ⚠ 警告" -ForegroundColor Yellow
    Write-Host "  端口 3306 已被占用（可修改配置）" -ForegroundColor Yellow
    $PassedChecks++
}
Write-Host ""

# 5. 检查环境配置文件
Write-Host "[5/8] 检查配置文件" -ForegroundColor Yellow
$TotalChecks++
if (Test-Path ".env") {
    Write-Host "检查 .env 文件 ... ✓ 通过" -ForegroundColor Green
    Write-Host "  .env 文件存在" -ForegroundColor Green
    $PassedChecks++
    
    # 检查是否使用默认密码
    $envContent = Get-Content ".env" -Raw
    if ($envContent -match "DB_PASSWORD=dormbill123") {
        Write-Host "  ⚠️  警告: 正在使用默认密码" -ForegroundColor Yellow
        Write-Host "     生产环境请修改 DB_PASSWORD" -ForegroundColor Yellow
    } else {
        Write-Host "  已设置自定义密码" -ForegroundColor Green
    }
} else {
    Write-Host "检查 .env 文件 ... ⚠ 警告" -ForegroundColor Yellow
    Write-Host "  .env 文件不存在" -ForegroundColor Yellow
    Write-Host "  运行: Copy-Item .env.docker .env" -ForegroundColor Yellow
    $PassedChecks++
}
Write-Host ""

# 6. 检查必需文件
Write-Host "[6/8] 检查项目文件" -ForegroundColor Yellow

$TotalChecks++
if (Test-Path "docker-compose.yml") {
    Write-Host "检查 docker-compose.yml ... ✓ 通过" -ForegroundColor Green
    $PassedChecks++
} else {
    Write-Host "检查 docker-compose.yml ... ✗ 失败" -ForegroundColor Red
    $FailedChecks++
}

$TotalChecks++
if (Test-Path "backend\Dockerfile") {
    Write-Host "检查 backend/Dockerfile ... ✓ 通过" -ForegroundColor Green
    $PassedChecks++
} else {
    Write-Host "检查 backend/Dockerfile ... ✗ 失败" -ForegroundColor Red
    $FailedChecks++
}

$TotalChecks++
if (Test-Path "frontend\Dockerfile") {
    Write-Host "检查 frontend/Dockerfile ... ✓ 通过" -ForegroundColor Green
    $PassedChecks++
} else {
    Write-Host "检查 frontend/Dockerfile ... ✗ 失败" -ForegroundColor Red
    $FailedChecks++
}

$TotalChecks++
if (Test-Path "docs\init_database.sql") {
    Write-Host "检查 docs/init_database.sql ... ✓ 通过" -ForegroundColor Green
    $PassedChecks++
} else {
    Write-Host "检查 docs/init_database.sql ... ✗ 失败" -ForegroundColor Red
    $FailedChecks++
}
Write-Host ""

# 7. 检查磁盘空间
Write-Host "[7/8] 检查磁盘空间" -ForegroundColor Yellow
$drive = (Get-Location).Drive
$freeSpace = [math]::Round(($drive.Free / 1GB), 2)
Write-Host "  可用空间: $freeSpace GB"

$TotalChecks++
if ($freeSpace -gt 5) {
    Write-Host "  ✓ 磁盘空间充足" -ForegroundColor Green
    $PassedChecks++
} else {
    Write-Host "  ⚠️  磁盘空间不足 5GB" -ForegroundColor Yellow
    $FailedChecks++
}
Write-Host ""

# 8. 检查容器状态
Write-Host "[8/8] 检查容器状态" -ForegroundColor Yellow
try {
    $containers = docker-compose ps 2>$null | Select-String "dormbill"
    if ($containers) {
        Write-Host "发现运行中的容器:" -ForegroundColor Green
        docker-compose ps
        Write-Host ""
        
        # 检查容器健康状态
        $healthy = docker-compose ps | Select-String "healthy"
        if ($healthy) {
            Write-Host "✓ 所有容器健康" -ForegroundColor Green
        } else {
            Write-Host "⚠️  部分容器未就绪，请等待..." -ForegroundColor Yellow
        }
    } else {
        Write-Host "未发现运行中的容器" -ForegroundColor Blue
        Write-Host "  运行以下命令启动:" -ForegroundColor Blue
        Write-Host "    docker-compose up -d" -ForegroundColor Blue
    }
} catch {
    Write-Host "未发现运行中的容器" -ForegroundColor Blue
}
Write-Host ""

# 总结
Write-Host "======================================" -ForegroundColor Blue
Write-Host "  检查完成" -ForegroundColor Blue
Write-Host "======================================" -ForegroundColor Blue
Write-Host "总检查项: $TotalChecks"
Write-Host "通过: $PassedChecks" -ForegroundColor Green
Write-Host "失败: $FailedChecks" -ForegroundColor Red
Write-Host ""

if ($FailedChecks -eq 0) {
    Write-Host "✓ 所有检查通过！您可以开始部署了。" -ForegroundColor Green
    Write-Host ""
    Write-Host "运行以下命令启动服务:"
    Write-Host "  docker-compose up -d"
    Write-Host ""
    Write-Host "或使用部署脚本:"
    Write-Host "  .\scripts\deploy.ps1 dev"
    exit 0
} else {
    Write-Host "⚠️  有 $FailedChecks 项检查未通过" -ForegroundColor Yellow
    Write-Host "请先解决上述问题，然后重新运行此脚本。"
    Write-Host ""
    Write-Host "获取帮助:"
    Write-Host "  查看文档: Get-Content QUICKSTART.md"
    Write-Host "  查看详细部署文档: Get-Content DOCKER_DEPLOY.md"
    exit 1
}
