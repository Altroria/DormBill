# 中文乱码问题修复指南

## 问题描述
前端"入住管理"页面显示的房间名称、员工姓名等中文字段出现乱码。

## 原因分析
1. 数据库连接时没有正确设置字符集
2. 导入 SQL 数据时字符集不一致
3. 数据库表的字符集不是 utf8mb4

## 解决方案

### 步骤 1: 上传修复文件到服务器

```bash
# 在本地执行，上传修复文件
scp backend/app/schemas/residence.py root@your-server:/root/workspace/DormBill/backend/app/schemas/
scp backend/app/routers/residences.py root@your-server:/root/workspace/DormBill/backend/app/routers/
scp scripts/fix_charset.sql root@your-server:/root/workspace/DormBill/scripts/
scp scripts/fix_residence_status.sql root@your-server:/root/workspace/DormBill/scripts/
scp scripts/diagnose_charset.sql root@your-server:/root/workspace/DormBill/scripts/
scp scripts/deploy_fix.sh root@your-server:/root/workspace/DormBill/scripts/
```

### 步骤 2: 诊断当前问题（可选）

```bash
# SSH 登录服务器
ssh root@your-server
cd /root/workspace/DormBill

# 运行诊断脚本，查看当前字符集配置
docker compose -f docker-compose.prod.yml exec mysql mysql -uroot -p405649 dormbill < scripts/diagnose_charset.sql
```

### 步骤 3: 执行自动修复

```bash
cd /root/workspace/DormBill

# 方式 1: 使用自动脚本（推荐）
chmod +x scripts/deploy_fix.sh
./scripts/deploy_fix.sh
```

### 步骤 4: 手动修复（如果自动脚本失败）

```bash
cd /root/workspace/DormBill

# 1. 修复数据库字符集
docker compose -f docker-compose.prod.yml exec -T mysql mysql -uroot -p405649 --default-character-set=utf8mb4 dormbill < scripts/fix_charset.sql

# 2. 修复 status 字段的 NULL 值
docker compose -f docker-compose.prod.yml exec -T mysql mysql -uroot -p405649 --default-character-set=utf8mb4 dormbill < scripts/fix_residence_status.sql

# 3. 重新构建并重启后端
docker compose -f docker-compose.prod.yml build backend
docker compose -f docker-compose.prod.yml up -d backend

# 4. 查看日志确认启动成功
docker compose -f docker-compose.prod.yml logs -f backend
```

### 步骤 5: 验证修复结果

1. 在服务器上检查数据：
```bash
docker compose -f docker-compose.prod.yml exec mysql mysql -uroot -p405649 dormbill -e "SELECT id, room_no, room_name FROM rooms WHERE room_name LIKE '%单间%' LIMIT 5;"
```

2. 在浏览器中刷新前端页面，检查"入住管理"列表是否正常显示中文

## 技术细节

### 修改的文件

1. **backend/app/schemas/residence.py**
   - 将 `status` 字段改为 `Optional[str]`，兼容 NULL 值

2. **backend/app/routers/residences.py**
   - 为 NULL 的 `status` 字段提供默认值 `"valid"`

3. **scripts/fix_charset.sql**
   - 修改数据库和所有表的字符集为 utf8mb4
   - 使用 `CONVERT TO CHARACTER SET` 转换已有数据

4. **scripts/fix_residence_status.sql**
   - 将所有 NULL 的 `status` 更新为 `"valid"`

### 预防措施

以后导入 SQL 数据时，确保：

```bash
# 使用 --default-character-set=utf8mb4 参数
docker compose -f docker-compose.prod.yml exec -T mysql \
  mysql -uroot -p405649 --default-character-set=utf8mb4 dormbill < your_script.sql
```

或在 SQL 脚本开头添加：
```sql
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
```

## 常见问题

### Q: 修复后仍然乱码？
A: 检查数据是否已经损坏。如果是，需要重新导入原始数据：
```bash
# 清空表
docker compose -f docker-compose.prod.yml exec mysql mysql -uroot -p405649 dormbill -e "TRUNCATE TABLE residence_records;"

# 重新导入（注意字符集参数）
docker compose -f docker-compose.prod.yml exec -T mysql \
  mysql -uroot -p405649 --default-character-set=utf8mb4 dormbill < scripts/import_residences.sql
```

### Q: 如何检查数据是否已损坏？
A: 使用 HEX 函数查看原始字节：
```bash
docker compose -f docker-compose.prod.yml exec mysql mysql -uroot -p405649 dormbill \
  -e "SELECT name, HEX(name) FROM employees LIMIT 3;"
```

如果 HEX 显示的是正确的 UTF-8 编码，说明数据正常，只是显示问题。

### Q: 需要重启整个应用吗？
A: 只需重启后端服务即可：
```bash
docker compose -f docker-compose.prod.yml restart backend
```

## 联系支持
如果问题仍未解决，请提供以下信息：
1. `diagnose_charset.sql` 的输出结果
2. 后端日志：`docker compose -f docker-compose.prod.yml logs backend --tail=100`
3. 前端浏览器控制台的错误信息
