# 快速操作命令 - 复制粘贴即可使用

## 步骤 1：上传文件到服务器

在本地 PowerShell 执行：
```powershell
scp E:\cursor\DormBill\dormbill_backup_20260923.sql root@47.102.36.185:/root/
```
输入服务器密码：`Sunhao49648`

---

## 步骤 2：SSH 连接服务器

```powershell
ssh root@47.102.36.185
```
输入密码：`Sunhao49648`

---

## 步骤 3：在服务器上导入（连接后执行）

### 3.1 查看 MySQL 容器名
```bash
docker ps | grep mysql
```

### 3.2 设置容器名（根据上面的输出调整）
```bash
# 常见容器名（根据实际情况选择）：
# MYSQL_CONTAINER=dormbill-mysql-1
# MYSQL_CONTAINER=dormbill_mysql_1
# MYSQL_CONTAINER=mysql
# MYSQL_CONTAINER=dormbill-db-1

MYSQL_CONTAINER=dormbill-mysql-1  # ⚠️ 修改为实际容器名
```

### 3.3 备份现有数据（推荐）
```bash
docker exec $MYSQL_CONTAINER mysqldump -uroot -p405649 --databases dormbill > backup_before_import_$(date +%Y%m%d_%H%M%S).sql 2>/dev/null || echo "无现有数据或首次部署"
```

### 3.4 导入数据
```bash
cd /root
docker exec -i $MYSQL_CONTAINER mysql -uroot -p405649 < dormbill_backup_20260923.sql
```

### 3.5 验证导入
```bash
docker exec $MYSQL_CONTAINER mysql -uroot -p405649 -e "USE dormbill; SHOW TABLES;"
```

### 3.6 重启后端服务（让应用使用新数据）
```bash
# 查看后端容器名
docker ps | grep backend

# 重启后端（根据实际容器名调整）
docker restart dormbill-backend-1
# 或者
# docker restart dormbill_backend_1
```

---

## 一键执行版本（设置好容器名后）

```bash
# 设置变量
MYSQL_CONTAINER=dormbill-mysql-1  # ⚠️ 修改为实际容器名
BACKEND_CONTAINER=dormbill-backend-1  # ⚠️ 修改为实际容器名
DB_PASSWORD=405649
BACKUP_FILE=/root/dormbill_backup_20260923.sql

# 执行导入
echo "==> 备份现有数据..."
docker exec $MYSQL_CONTAINER mysqldump -uroot -p${DB_PASSWORD} --databases dormbill > backup_$(date +%Y%m%d_%H%M%S).sql 2>/dev/null || echo "无现有数据"

echo "==> 导入新数据..."
docker exec -i $MYSQL_CONTAINER mysql -uroot -p${DB_PASSWORD} < $BACKUP_FILE

echo "==> 验证导入..."
docker exec $MYSQL_CONTAINER mysql -uroot -p${DB_PASSWORD} -e "USE dormbill; SHOW TABLES;"

echo "==> 重启后端服务..."
docker restart $BACKEND_CONTAINER

echo "==> 完成！"
```

---

## 问题排查

### 如果提示"容器不存在"
```bash
# 列出所有运行中的容器
docker ps

# 找到包含 mysql 的容器名，复制准确的名称
```

### 如果导入报错
```bash
# 查看 MySQL 容器日志
docker logs $MYSQL_CONTAINER --tail 50

# 手动进入容器测试
docker exec -it $MYSQL_CONTAINER bash
mysql -uroot -p405649
# 输入密码后：
SHOW DATABASES;
USE dormbill;
SHOW TABLES;
exit
exit
```

### 如果忘记备份想回滚
```bash
# 使用之前创建的备份
ls -lh backup_*.sql
docker exec -i $MYSQL_CONTAINER mysql -uroot -p405649 < backup_20260923_XXXXXX.sql
```
