# SSH连接并导入数据
# 复制下面的命令到 PowerShell 执行

# 连接服务器
ssh root@47.102.36.185

# 连接成功后，在服务器上执行以下命令：
# =========================================

# 1. 查看MySQL容器名
docker ps

# 2. 根据上面的输出，找到MySQL容器名，然后设置变量（修改容器名）
MYSQL_CONTAINER=dormbill-mysql-1

# 3. 备份现有数据（安全起见）
docker exec $MYSQL_CONTAINER mysqldump -uroot -p405649 --databases dormbill > backup_before_import.sql 2>/dev/null || echo "无现有数据或首次部署"

# 4. 导入数据
docker exec -i $MYSQL_CONTAINER mysql -uroot -p405649 < /root/dormbill_backup_20260923.sql

# 5. 验证导入
docker exec $MYSQL_CONTAINER mysql -uroot -p405649 -e "USE dormbill; SHOW TABLES;"

# 6. 查看数据行数
docker exec $MYSQL_CONTAINER mysql -uroot -p405649 dormbill -e "SELECT 'buildings' as tbl, COUNT(*) as cnt FROM buildings UNION ALL SELECT 'rooms', COUNT(*) FROM rooms UNION ALL SELECT 'employees', COUNT(*) FROM employees UNION ALL SELECT 'residences', COUNT(*) FROM residences;"

# 7. 重启后端服务
docker ps | grep backend
docker restart dormbill-backend-1

echo "✅ 导入完成！"
