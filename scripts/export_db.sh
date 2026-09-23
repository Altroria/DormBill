#!/bin/bash
# 导出本地数据库脚本

DB_NAME="dorm_management"
DB_USER="root"
BACKUP_FILE="dorm_backup_$(date +%Y%m%d_%H%M%S).sql"

echo "开始导出数据库 $DB_NAME..."
mysqldump -u $DB_USER -p $DB_NAME > $BACKUP_FILE

if [ $? -eq 0 ]; then
    echo "✅ 导出成功: $BACKUP_FILE"
    echo "文件大小: $(du -h $BACKUP_FILE | cut -f1)"
else
    echo "❌ 导出失败"
    exit 1
fi
