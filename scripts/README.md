# 数据库导入导出脚本

## 使用场景
将本地开发环境的MySQL数据导入到服务器Docker部署的MySQL容器中。

## 操作步骤

### 1. 导出本地数据

**Windows:**
```bash
cd E:\cursor\DormBill\scripts
export_db.bat
# 输入MySQL密码，会生成 dorm_backup_YYYYMMDD_HHMMSS.sql 文件
```

**Linux/Mac:**
```bash
cd /path/to/DormBill/scripts
chmod +x export_db.sh
./export_db.sh
# 输入MySQL密码，会生成 dorm_backup_YYYYMMDD_HHMMSS.sql 文件
```

### 2. 上传到服务器

```bash
# 使用 scp 上传
scp dorm_backup_*.sql user@your-server:/home/user/

# 或使用 FTP/SFTP 工具上传
```

### 3. 在服务器上导入

**方法A: 使用导入脚本**
```bash
# 上传 import_to_docker.sh 到服务器
chmod +x import_to_docker.sh

# 修改脚本中的配置
# MYSQL_CONTAINER: MySQL容器名（docker ps 查看）
# DB_PASSWORD: 数据库密码

# 执行导入
./import_to_docker.sh dorm_backup_*.sql
```

**方法B: 手动导入**
```bash
# 查看MySQL容器名
docker ps | grep mysql

# 导入数据（推荐方式）
docker exec -i mysql-container mysql -uroot -p数据库密码 dorm_management < dorm_backup.sql

# 或者分两步
docker cp dorm_backup.sql mysql-container:/tmp/
docker exec -it mysql-container bash
mysql -uroot -p dorm_management < /tmp/dorm_backup.sql
```

## 注意事项

1. **备份线上数据**：导入前先备份线上现有数据
   ```bash
   docker exec mysql-container mysqldump -uroot -p密码 dorm_management > online_backup.sql
   ```

2. **检查字符集**：确保本地和线上MySQL字符集一致（建议 utf8mb4）

3. **检查数据库版本**：本地和线上MySQL版本差异不要太大

4. **大文件导入**：如果SQL文件很大，可以压缩后再传输
   ```bash
   gzip dorm_backup.sql
   scp dorm_backup.sql.gz user@server:/path/
   gunzip dorm_backup.sql.gz
   ```

5. **权限问题**：确保有足够的权限访问Docker容器

## 验证数据

导入后验证数据：
```bash
docker exec -it mysql-container mysql -uroot -p

USE dorm_management;
SHOW TABLES;
SELECT COUNT(*) FROM employees;
SELECT COUNT(*) FROM buildings;
# ... 检查其他表
```

## 故障排查

### 导入失败
- 检查容器是否运行：`docker ps`
- 检查容器日志：`docker logs mysql-container`
- 检查SQL文件编码：应为 UTF-8
- 尝试分批导入：将大SQL文件拆分

### 字符乱码
```sql
-- 检查字符集
SHOW VARIABLES LIKE 'character%';

-- 如需修改
ALTER DATABASE dorm_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
