#!/bin/bash
# 
# DormBill 部署脚本 (Linux/macOS)
# 
# 使用方法:
#   ./scripts/deploy.sh dev     # 开发环境部署
#   ./scripts/deploy.sh prod    # 生产环境部署
#   ./scripts/deploy.sh stop    # 停止服务
#   ./scripts/deploy.sh restart # 重启服务
#   ./scripts/deploy.sh logs    # 查看日志
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查 Docker 是否安装
check_docker() {
    if ! command -v docker &> /dev/null; then
        log_error "Docker 未安装，请先安装 Docker"
        exit 1
    fi

    # 检测使用哪个 docker-compose 命令
    if command -v docker-compose &> /dev/null; then
        DOCKER_COMPOSE="docker-compose"
    elif docker compose version &> /dev/null 2>&1; then
        DOCKER_COMPOSE="docker compose"
    else
        log_error "Docker Compose 未安装，请先安装 Docker Compose"
        exit 1
    fi
    
    log_info "使用 Docker Compose: $DOCKER_COMPOSE"
}

# 检查环境变量文件
check_env() {
    if [ ! -f .env ]; then
        log_warn ".env 文件不存在，从 .env.docker 复制"
        cp .env.docker .env
        log_info "已创建 .env 文件，请根据实际情况修改配置"
        read -p "按 Enter 键继续..."
    fi
}

# 开发环境部署
deploy_dev() {
    log_info "开始部署开发环境..."
    check_docker
    check_env

    log_info "构建并启动服务..."
    $DOCKER_COMPOSE up -d --build

    log_info "等待服务启动..."
    sleep 10

    log_info "检查服务状态..."
    $DOCKER_COMPOSE ps

    log_info ""
    log_info "=========================================="
    log_info "开发环境部署完成！"
    log_info "=========================================="
    log_info "前端访问: http://localhost"
    log_info "后端 API: http://localhost:8000/docs"
    log_info "健康检查: http://localhost:8000/health"
    log_info "=========================================="
    log_info ""
    log_info "查看日志: $DOCKER_COMPOSE logs -f"
}

# 生产环境部署
deploy_prod() {
    log_info "开始部署生产环境..."
    check_docker
    check_env

    # 检查必需的环境变量
    if grep -q "DB_PASSWORD=dormbill123" .env; then
        log_error "请修改 .env 中的 DB_PASSWORD 为强密码！"
        exit 1
    fi

    log_info "拉取最新代码..."
    if [ -d .git ]; then
        git pull
    fi

    log_info "构建并启动服务（生产配置）..."
    $DOCKER_COMPOSE -f docker-compose.prod.yml up -d --build

    log_info "等待服务启动..."
    sleep 15

    log_info "检查服务状态..."
    $DOCKER_COMPOSE -f docker-compose.prod.yml ps

    log_info ""
    log_info "=========================================="
    log_info "生产环境部署完成！"
    log_info "=========================================="
    log_info "前端访问: http://localhost"
    log_info "=========================================="
    log_info ""
    log_info "查看日志: $DOCKER_COMPOSE -f docker-compose.prod.yml logs -f"
}

# 停止服务
stop_services() {
    log_info "停止服务..."
    check_docker
    
    if $DOCKER_COMPOSE ps 2>/dev/null | grep -q "Up"; then
        $DOCKER_COMPOSE stop
        log_info "开发环境已停止"
    fi

    if $DOCKER_COMPOSE -f docker-compose.prod.yml ps 2>/dev/null | grep -q "Up"; then
        $DOCKER_COMPOSE -f docker-compose.prod.yml stop
        log_info "生产环境已停止"
    fi

    log_info "服务已停止"
}

# 重启服务
restart_services() {
    log_info "重启服务..."
    check_docker
    
    if $DOCKER_COMPOSE ps 2>/dev/null | grep -q "dormbill"; then
        $DOCKER_COMPOSE restart
        log_info "开发环境已重启"
    elif $DOCKER_COMPOSE -f docker-compose.prod.yml ps 2>/dev/null | grep -q "dormbill"; then
        $DOCKER_COMPOSE -f docker-compose.prod.yml restart
        log_info "生产环境已重启"
    else
        log_error "未找到运行中的服务"
        exit 1
    fi
}

# 查看日志
view_logs() {
    check_docker
    if $DOCKER_COMPOSE ps 2>/dev/null | grep -q "dormbill"; then
        $DOCKER_COMPOSE logs -f --tail=100
    elif $DOCKER_COMPOSE -f docker-compose.prod.yml ps 2>/dev/null | grep -q "dormbill"; then
        $DOCKER_COMPOSE -f docker-compose.prod.yml logs -f --tail=100
    else
        log_error "未找到运行中的服务"
        exit 1
    fi
}

# 备份数据库
backup_database() {
    log_info "开始备份数据库..."
    check_docker
    
    BACKUP_DIR="backups"
    mkdir -p "$BACKUP_DIR"
    
    BACKUP_FILE="$BACKUP_DIR/dormbill_$(date +%Y%m%d_%H%M%S).sql"
    
    if $DOCKER_COMPOSE ps 2>/dev/null | grep -q "dormbill-mysql"; then
        source .env
        $DOCKER_COMPOSE exec -T mysql mysqldump -uroot -p"${DB_PASSWORD}" dormbill > "$BACKUP_FILE"
    elif $DOCKER_COMPOSE -f docker-compose.prod.yml ps 2>/dev/null | grep -q "dormbill-mysql"; then
        source .env
        $DOCKER_COMPOSE -f docker-compose.prod.yml exec -T mysql mysqldump -uroot -p"${DB_PASSWORD}" dormbill > "$BACKUP_FILE"
    else
        log_error "MySQL 容器未运行"
        exit 1
    fi
    
    log_info "数据库备份完成: $BACKUP_FILE"
}

# 显示帮助信息
show_help() {
    echo "DormBill 部署脚本"
    echo ""
    echo "使用方法:"
    echo "  ./scripts/deploy.sh <command>"
    echo ""
    echo "可用命令:"
    echo "  dev      - 部署开发环境"
    echo "  prod     - 部署生产环境"
    echo "  stop     - 停止服务"
    echo "  restart  - 重启服务"
    echo "  logs     - 查看日志"
    echo "  backup   - 备份数据库"
    echo "  help     - 显示此帮助信息"
}

# 主逻辑
case "$1" in
    dev)
        deploy_dev
        ;;
    prod)
        deploy_prod
        ;;
    stop)
        stop_services
        ;;
    restart)
        restart_services
        ;;
    logs)
        view_logs
        ;;
    backup)
        backup_database
        ;;
    help|--help|-h|"")
        show_help
        ;;
    *)
        log_error "未知命令: $1"
        show_help
        exit 1
        ;;
esac
