# 快速修复中文乱码

## 在服务器上执行以下命令：

```bash
cd /root/workspace/DormBill

# 1. 修复数据库字符集
docker compose -f docker-compose.prod.yml exec mysql mysql -uroot -p405649 --default-character-set=utf8mb4 dormbill -e "
ALTER DATABASE dormbill CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
ALTER TABLE buildings CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE rooms CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE employees CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE residence_records CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
UPDATE residence_records SET status = 'valid' WHERE status IS NULL;
"

# 2. 重启后端服务
docker compose -f docker-compose.prod.yml restart backend

# 3. 查看后端日志
docker compose -f docker-compose.prod.yml logs backend --tail=30
```

## 验证修复：

```bash
# 查看数据是否正常
docker compose -f docker-compose.prod.yml exec mysql mysql -uroot -p405649 dormbill -e "SELECT id, room_no, room_name FROM rooms LIMIT 5;"
```

如果看到中文正常显示，刷新前端页面即可。

---

## 如果上述命令无效，需要上传修复文件：

```bash
# 在本地执行（替换 your-server 为实际服务器地址）
cd E:\cursor\DormBill

scp backend/app/schemas/residence.py root@your-server:/root/workspace/DormBill/backend/app/schemas/
scp backend/app/routers/residences.py root@your-server:/root/workspace/DormBill/backend/app/routers/
scp scripts/fix_charset.sql root@your-server:/root/workspace/DormBill/scripts/
scp scripts/fix_residence_status.sql root@your-server:/root/workspace/DormBill/scripts/

# 然后在服务器上执行
cd /root/workspace/DormBill
docker compose -f docker-compose.prod.yml exec -T mysql mysql -uroot -p405649 --default-character-set=utf8mb4 dormbill < scripts/fix_charset.sql
docker compose -f docker-compose.prod.yml exec -T mysql mysql -uroot -p405649 --default-character-set=utf8mb4 dormbill < scripts/fix_residence_status.sql
docker compose -f docker-compose.prod.yml build backend
docker compose -f docker-compose.prod.yml up -d backend
```
