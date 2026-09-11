#!/bin/bash
# 部署修复脚本

echo "=== 步骤 1: 修复数据库字符集 ==="
docker compose -f docker-compose.prod.yml exec -T mysql mysql -uroot -p405649 --default-character-set=utf8mb4 dormbill < scripts/fix_charset.sql

echo ""
echo "=== 步骤 2: 修复数据库中的 NULL status ==="
docker compose -f docker-compose.prod.yml exec -T mysql mysql -uroot -p405649 --default-character-set=utf8mb4 dormbill < scripts/fix_residence_status.sql

echo ""
echo "=== 步骤 3: 重新构建后端服务 ==="
docker compose -f docker-compose.prod.yml build backend

echo ""
echo "=== 步骤 4: 重启后端服务 ==="
docker compose -f docker-compose.prod.yml up -d backend

echo ""
echo "=== 步骤 5: 查看后端日志 ==="
docker compose -f docker-compose.prod.yml logs backend --tail=30

echo ""
echo "=== 修复完成 ==="
echo "请在前端刷新页面测试入住列表功能"
