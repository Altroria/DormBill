#!/bin/bash
#
# DormBill Docker 环境检查脚本
# 使用方法: ./scripts/check-docker.sh
#

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}  DormBill Docker 环境检查${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""

# 检查项计数
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0

# 检查函数
check_item() {
    local name=$1
    local command=$2
    
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    
    echo -n "检查 $name ... "
    
    if eval "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ 通过${NC}"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
        return 0
    else
        echo -e "${RED}✗ 失败${NC}"
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
        return 1
    fi
}

# 1. 检查 Docker
echo -e "${YELLOW}[1/8] 检查 Docker 安装${NC}"
if check_item "Docker" "docker --version"; then
    DOCKER_VERSION=$(docker --version)
    echo "  版本: $DOCKER_VERSION"
else
    echo -e "  ${RED}请安装 Docker: https://www.docker.com/products/docker-desktop${NC}"
fi
echo ""

# 2. 检查 Docker Compose
echo -e "${YELLOW}[2/8] 检查 Docker Compose${NC}"
if check_item "Docker Compose" "docker-compose --version || docker compose version"; then
    COMPOSE_VERSION=$(docker-compose --version 2>/dev/null || docker compose version 2>/dev/null)
    echo "  版本: $COMPOSE_VERSION"
else
    echo -e "  ${RED}请安装 Docker Compose${NC}"
fi
echo ""

# 3. 检查 Docker 服务状态
echo -e "${YELLOW}[3/8] 检查 Docker 服务${NC}"
if check_item "Docker 守护进程" "docker info"; then
    echo -e "  ${GREEN}Docker 服务正在运行${NC}"
else
    echo -e "  ${RED}Docker 服务未启动，请启动 Docker Desktop${NC}"
fi
echo ""

# 4. 检查端口占用
echo -e "${YELLOW}[4/8] 检查端口占用${NC}"

check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1 || netstat -tuln 2>/dev/null | grep -q ":$port "; then
        return 1
    else
        return 0
    fi
}

if check_item "端口 80 (前端)" "check_port 80"; then
    echo -e "  ${GREEN}端口 80 可用${NC}"
else
    echo -e "  ${RED}端口 80 已被占用${NC}"
    echo "  运行以下命令查看占用进程:"
    echo "    Linux/macOS: sudo lsof -i :80"
    echo "    Windows: netstat -ano | findstr :80"
fi

if check_item "端口 8000 (后端)" "check_port 8000"; then
    echo -e "  ${GREEN}端口 8000 可用${NC}"
else
    echo -e "  ${YELLOW}端口 8000 已被占用（可选端口，不影响使用）${NC}"
fi

if check_item "端口 3306 (MySQL)" "check_port 3306"; then
    echo -e "  ${GREEN}端口 3306 可用${NC}"
else
    echo -e "  ${YELLOW}端口 3306 已被占用（可修改配置）${NC}"
fi
echo ""

# 5. 检查环境配置文件
echo -e "${YELLOW}[5/8] 检查配置文件${NC}"
if check_item ".env 文件" "test -f .env"; then
    echo -e "  ${GREEN}.env 文件存在${NC}"
    
    # 检查是否使用默认密码
    if grep -q "DB_PASSWORD=dormbill123" .env 2>/dev/null; then
        echo -e "  ${YELLOW}⚠️  警告: 正在使用默认密码${NC}"
        echo -e "  ${YELLOW}   生产环境请修改 DB_PASSWORD${NC}"
    else
        echo -e "  ${GREEN}已设置自定义密码${NC}"
    fi
else
    echo -e "  ${YELLOW}.env 文件不存在${NC}"
    echo -e "  运行: cp .env.docker .env"
fi
echo ""

# 6. 检查必需文件
echo -e "${YELLOW}[6/8] 检查项目文件${NC}"
check_item "docker-compose.yml" "test -f docker-compose.yml"
check_item "backend/Dockerfile" "test -f backend/Dockerfile"
check_item "frontend/Dockerfile" "test -f frontend/Dockerfile"
check_item "docs/init_database.sql" "test -f docs/init_database.sql"
echo ""

# 7. 检查磁盘空间
echo -e "${YELLOW}[7/8] 检查磁盘空间${NC}"
AVAILABLE_SPACE=$(df -h . | awk 'NR==2 {print $4}')
echo "  可用空间: $AVAILABLE_SPACE"

# 转换为 GB 进行比较（简化）
SPACE_GB=$(df -BG . | awk 'NR==2 {print $4}' | sed 's/G//')
if [ "$SPACE_GB" -gt 5 ]; then
    echo -e "  ${GREEN}✓ 磁盘空间充足${NC}"
    PASSED_CHECKS=$((PASSED_CHECKS + 1))
else
    echo -e "  ${YELLOW}⚠️  磁盘空间不足 5GB${NC}"
fi
TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
echo ""

# 8. 检查容器状态
echo -e "${YELLOW}[8/8] 检查容器状态${NC}"
if docker-compose ps 2>/dev/null | grep -q "dormbill"; then
    echo -e "${GREEN}发现运行中的容器:${NC}"
    docker-compose ps
    echo ""
    
    # 检查容器健康状态
    if docker-compose ps | grep -q "healthy"; then
        echo -e "${GREEN}✓ 所有容器健康${NC}"
    else
        echo -e "${YELLOW}⚠️  部分容器未就绪，请等待...${NC}"
    fi
else
    echo -e "${BLUE}未发现运行中的容器${NC}"
    echo "  运行以下命令启动:"
    echo "    docker-compose up -d"
fi
echo ""

# 总结
echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}  检查完成${NC}"
echo -e "${BLUE}======================================${NC}"
echo -e "总检查项: $TOTAL_CHECKS"
echo -e "${GREEN}通过: $PASSED_CHECKS${NC}"
echo -e "${RED}失败: $FAILED_CHECKS${NC}"
echo ""

if [ $FAILED_CHECKS -eq 0 ]; then
    echo -e "${GREEN}✓ 所有检查通过！您可以开始部署了。${NC}"
    echo ""
    echo "运行以下命令启动服务:"
    echo "  docker-compose up -d"
    echo ""
    echo "或使用部署脚本:"
    echo "  ./scripts/deploy.sh dev"
    exit 0
else
    echo -e "${YELLOW}⚠️  有 $FAILED_CHECKS 项检查未通过${NC}"
    echo "请先解决上述问题，然后重新运行此脚本。"
    echo ""
    echo "获取帮助:"
    echo "  查看文档: cat QUICKSTART.md"
    echo "  查看详细部署文档: cat DOCKER_DEPLOY.md"
    exit 1
fi
