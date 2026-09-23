# 数据库迁移指南

## 📋 概述

将本地 MySQL 数据库导入到线上 Docker 部署的 MySQL 容器。

**服务器信息：**
- IP: 47.102.36.185
- 用户: root
- 数据库: dormbill
- MySQL 密码: 405649

---

## 🚀 操作步骤

### 步骤 1：本地导出数据（已完成 ✅）

已导出文件：`E:\cursor\DormBill\dormbill_backup_20260923.sql` (77.33 KB)

### 步骤 2：上传文件到服务器

**方式 A：使用 scp（推荐）**

在本地 PowerShell 执行：

```powershell
scp E:\cursor\DormBill\dormbill_backup_20260923.sql root@47.102.36.185:/root/
```

**方式 B：使用 WinSCP 或 FileZilla**

1. 打开 WinSCP/FileZilla
2. 连接到 `47.102.36.185`，用户 `root`，密码 `Sunhao49648`
3. 上传 `dormbill_backup_20260923.sql` 到 `/root/` 目录

### 步骤 3：在服务器上导入数据

**SSH 连接到服务器：**

```bash
ssh root@47.102.36.185
```

**执行导入（三种方式，任选一种）：**

#### 方式 1：直接导入（最简单）

```bash
# 先查看 MySQL 容器名
docker ps | grep mysql

# 假设容器名是 dormbill-mysql-1 或 mysql（根据实际输出调整）
MYSQL_CONTAINER=dormbill-mysql-1

# 导入数据
docker exec -i $MYSQL_CONTAINER mysql -uroot -p405649 dormbill < /root/dormbill_backup_20260923.sql

# 验证导入
docker exec $MYSQL_CONTAINER mysql -uroot -p405649 -e "USE dormbill; SHOW TABLES;"
```

#### 方式 2：使用自动化脚本

上传 `scripts/import_to_server.sh` 到服务器，然后：

```bash
chmod +x import_to_server.sh
./import_to_server.sh
```

#### 方式 3：进入容器内部导入

```bash
# 复制文件到容器
docker cp /root/dormbill_backup_20260923.sql $MYSQL_CONTAINER:/tmp/

# 进入容器
docker exec -it $MYSQL_CONTAINER bash

# 在容器内导入
mysql -uroot -p405649 < /tmp/dormbill_backup_20260923.sql

# 验证
mysql -uroot -p405649 -e "USE dormbill; SHOW TABLES;"

# 退出容器
exit
```

---

## ⚠️ 重要提醒

### 导入前检查清单

- [ ] **备份线上现有数据**（如果已有数据）
  ```bash
  docker exec $MYSQL_CONTAINER mysqldump -uroot -p405649 --databases dormbill > backup_before_import.sql
  ```

- [ ] **确认容器名称**
  ```bash
  docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}"
  ```

- [ ] **确认数据库名称一致**（都是 `dormbill`）

- [ ] **检查字符集**（确保是 utf8mb4）
  ```bash
  docker exec $MYSQL_CONTAINER mysql -uroot -p405649 -e "SHOW CREATE DATABASE dormbill;"
  ```

### 常见问题排查

**问题 1：找不到容器**
```bash
# 查看所有容器（包括停止的）
docker ps -a

# 启动停止的容器
docker start <container_name>
```

**问题 2：权限错误**
```bash
# 检查文件权限
ls -lh dormbill_backup_20260923.sql
chmod 644 dormbill_backup_20260923.sql
```

**问题 3：数据库已存在冲突**
```bash
# 删除现有数据库（谨慎！）
docker exec $MYSQL_CONTAINER mysql -uroot -p405649 -e "DROP DATABASE IF EXISTS dormbill;"

# 重新导入
docker exec -i $MYSQL_CONTAINER mysql -uroot -p405649 < dormbill_backup_20260923.sql
```

**问题 4：容器内存不足**
```bash
# 检查容器资源
docker stats $MYSQL_CONTAINER

# 如果文件很大，分批导入或增加容器内存
```

---

## ✅ 验证导入成功

导入完成后，执行以下命令验证：

```bash
# 1. 检查数据库
docker exec $MYSQL_CONTAINER mysql -uroot -p405649 -e "SHOW DATABASES;"

# 2. 检查表
docker exec $MYSQL_CONTAINER mysql -uroot -p405649 -e "USE dormbill; SHOW TABLES;"

# 3. 检查数据行数
docker exec $MYSQL_CONTAINER mysql -uroot -p405649 dormbill -e "
SELECT 
  'buildings' as table_name, COUNT(*) as count FROM buildings
  UNION ALL SELECT 'rooms', COUNT(*) FROM rooms
  UNION ALL SELECT 'employees', COUNT(*) FROM employees
  UNION ALL SELECT 'residences', COUNT(*) FROM residences;
"

# 4. 测试应用连接
# 重启后端服务
docker restart dormbill-backend-1  # 根据实际容器名调整
```

---

## 🔄 回滚操作

如果导入出现问题，需要回滚：

```bash
# 使用之前的备份恢复
docker exec -i $MYSQL_CONTAINER mysql -uroot -p405649 < backup_before_import.sql
```

---

## 📞 需要帮助？

- 确认 MySQL 容器名：`docker ps | grep mysql`
- 查看容器日志：`docker logs $MYSQL_CONTAINER`
- 查看导入错误：导入命令后会显示错误信息
