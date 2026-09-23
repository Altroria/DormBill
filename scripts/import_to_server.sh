#!/bin/bash
# 服务器端导入脚本
# 在服务器上运行此脚本导入数据

set -e

DB_NAME="dormbill"
DB_PASSWORD="405649"
BACKUP_FILE="dormbill_backup_20260923.sql"

echo "=================================="
echo "MySQL 数据导入工具 (Docker)"
echo "=================================="
echo ""

# 检查备份文件是否存在
if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ 找不到备份文件: $BACKUP_FILE"
    echo "请先上传备份文件到当前目录"
    exit 1
fi

echo "备份文件: $BACKUP_FILE"
echo "数据库: $DB_NAME"
echo ""

# 查找 MySQL 容器
echo "正在查找 MySQL 容器..."
MYSQL_CONTAINER=$(docker ps --filter "ancestor=mysql" --format "{{.Names}}" | head -n 1)

if [ -z "$MYSQL_CONTAINER" ]; then
    # 尝试通过名称模糊匹配
    MYSQL_CONTAINER=$(docker ps --format "{{.Names}}" | grep -i mysql | head -n 1)
fi

if [ -z "$MYSQL_CONTAINER" ]; then
    echo "❌ 找不到运行中的 MySQL 容器"
    echo ""
    echo "运行中的容器列表："
    docker ps --format "table {{.Names}}\t{{.Image}}"
    exit 1
fi

echo "✅ 找到 MySQL 容器: $MYSQL_CONTAINER"
echo ""

# 备份现有数据（可选但强烈推荐）
echo "⚠️  准备备份现有数据..."
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
CURRENT_BACKUP="dormbill_before_import_${TIMESTAMP}.sql"

docker exec $MYSQL_CONTAINER mysqldump -uroot -p${DB_PASSWORD} --databases $DB_NAME --add-drop-database > $CURRENT_BACKUP 2>/dev/null || true

if [ -f "$CURRENT_BACKUP" ] && [ -s "$CURRENT_BACKUP" ]; then
    echo "✅ 已备份现有数据到: $CURRENT_BACKUP"
else
    echo "ℹ️  没有现有数据或备份失败（首次部署时正常）"
    rm -f $CURRENT_BACKUP
fi
echo ""

# 导入数据
echo "正在导入数据..."
docker exec -i $MYSQL_CONTAINER mysql -uroot -p${DB_PASSWORD} < $BACKUP_FILE

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 数据导入成功！"
    echo ""
    echo "验证导入..."
    docker exec $MYSQL_CONTAINER mysql -uroot -p${DB_PASSWORD} -e "USE $DB_NAME; SHOW TABLES;"
    echo ""
    echo "🎉 全部完成！"
else
    echo ""
    echo "❌ 导入失败"
    exit 1
fi
