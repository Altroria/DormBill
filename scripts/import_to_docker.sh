#!/bin/bash
# 导入数据到Docker MySQL容器

# 配置参数
MYSQL_CONTAINER="mysql"  # 修改为你的MySQL容器名
DB_NAME="dorm_management"
DB_USER="root"
DB_PASSWORD="your_password"  # 修改为实际密码
BACKUP_FILE=$1

if [ -z "$BACKUP_FILE" ]; then
    echo "用法: ./import_to_docker.sh <backup_file.sql>"
    exit 1
fi

if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ 文件不存在: $BACKUP_FILE"
    exit 1
fi

echo "开始导入数据到Docker容器 $MYSQL_CONTAINER..."
echo "数据库: $DB_NAME"
echo "文件: $BACKUP_FILE"

# 方式1: 使用管道直接导入（推荐）
cat "$BACKUP_FILE" | docker exec -i $MYSQL_CONTAINER mysql -u$DB_USER -p$DB_PASSWORD $DB_NAME

if [ $? -eq 0 ]; then
    echo "✅ 导入成功"
else
    echo "❌ 导入失败"
    exit 1
fi
