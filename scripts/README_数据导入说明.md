# 数据导入说明

## 概述

本目录包含从 Excel 文件生成数据库导入 SQL 脚本的工具。

## 文件说明

- **generate_import_sql.py** - Python 脚本，读取 Excel 文件并生成 SQL 导入脚本
- **import_all_data.sql** - 自动生成的 SQL 导入脚本（包含所有基础数据）

## 生成的数据统计

根据 `data/房间和人员数据.xlsx` 生成：

- **楼栋数量**: 5 个（247、248、249、250、99号楼）
- **房间数量**: 98 个房间
- **员工数量**: 121 名员工
- **入住记录**: 122 条入住记录

## 使用步骤

### 1. 重新生成 SQL 脚本（可选）

如果 Excel 数据有更新，可以重新生成：

```bash
cd scripts
python generate_import_sql.py
```

### 2. 准备数据库

确保已经创建数据库并运行了所有迁移：

```bash
# 进入后端目录
cd backend

# 运行数据库迁移
alembic upgrade head
```

### 3. 导入数据

**方式一：使用 MySQL 命令行工具**

```bash
# Windows PowerShell
cd E:\Cursor\DormBill\scripts
mysql -u root -p dormbill < import_all_data.sql

# 或指定主机
mysql -h localhost -u root -p dormbill < import_all_data.sql
```

**方式二：使用 MySQL Workbench**

1. 打开 MySQL Workbench
2. 连接到数据库
3. 打开 `import_all_data.sql` 文件
4. 执行整个脚本

**方式三：使用 Python 脚本导入（推荐用于开发环境）**

```python
import mysql.connector

config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',
    'database': 'dormbill'
}

conn = mysql.connector.connect(**config)
cursor = conn.cursor()

with open('import_all_data.sql', 'r', encoding='utf-8') as f:
    sql_script = f.read()
    
# 执行多条 SQL 语句
for statement in sql_script.split(';'):
    if statement.strip():
        cursor.execute(statement)

conn.commit()
cursor.close()
conn.close()
```

## 数据表结构映射

### 楼栋表 (buildings)

| Excel 列 | 数据库字段 | 说明 |
|---------|-----------|------|
| 楼号 | building_no | 楼栋编号 |
| - | name | 楼栋名称（自动生成） |
| - | address | 地址（自动生成） |
| - | status | 状态（默认 active） |

### 房间表 (rooms)

| Excel 列 | 数据库字段 | 说明 |
|---------|-----------|------|
| 楼号 | building_id | 外键关联 buildings |
| 房号 | room_no | 房间号码 |
| 室号 | room_unit | 室号/单元号 |
| 房间 | room_name | 房间名称 |
| 房租 | rent_standard | 房租标准 |
| - | electricity_price | 电价（默认 0.49） |
| - | status | 状态（默认 active） |

### 员工表 (employees)

| Excel 列 | 数据库字段 | 说明 |
|---------|-----------|------|
| - | employee_no | 工号（自动生成 EMP1001-） |
| 姓名 | name | 员工姓名 |
| 任职单位 | company | 任职单位 |
| 一级部门 | department | 一级部门 |
| 职务 | position | 职务 |
| 转宿日期，备注 | remark | 备注信息 |
| - | status | 状态（默认 active） |

### 入住记录表 (residence_records)

| Excel 列 | 数据库字段 | 说明 |
|---------|-----------|------|
| 姓名 | employee_id | 外键关联 employees |
| 楼号+房号+室号 | room_id | 外键关联 rooms |
| - | check_in_date | 入住日期（默认 2024-01-01） |
| - | check_out_date | 搬离日期（NULL） |
| 房租 > 0 | is_primary_payer | 是否主要缴费人 |
| 备注"试用"/"前3月" | probation_months | 试用期月数 |
| 备注"离宿" | status | 状态（valid/invalid） |
| 转宿日期，备注 | remark | 备注信息 |

## 数据处理规则

### 楼栋处理
- 从 Excel 的"楼号"列提取唯一值
- 自动生成楼栋名称（如"247号楼"）
- 99号楼标记为"特殊宿舍区"

### 房间处理
- 去重：同一个（楼号、房号、室号）只生成一条记录
- 默认电价：0.49 元/度
- 房租标准：从 Excel 的"房租"列获取

### 员工处理
- 去重：同一个姓名只生成一条员工记录
- 自动生成工号：EMP1001, EMP1002, ...
- 保留备注信息（夫妻间、试用期等）

### 入住记录处理
- **主要缴费人判断**：房租 > 0 为主缴费人（is_primary_payer = 1）
- **试用期识别**：备注中包含"试用"、"前3个月"、"前三个月"时，设置 probation_months = 3
- **状态判断**：备注中包含"离宿"时，status = 'invalid'，否则为 'valid'
- **入住日期**：默认设为 2024-01-01（实际使用时可手动调整）

## 注意事项

⚠️ **重要提醒**

1. **数据清空**：脚本会清空以下表的所有数据（TRUNCATE）：
   - residence_records
   - employees
   - rooms
   - buildings

2. **执行前备份**：建议先备份数据库
   ```bash
   mysqldump -u root -p dormbill > backup_$(date +%Y%m%d_%H%M%S).sql
   ```

3. **外键约束**：脚本会临时禁用外键检查（SET FOREIGN_KEY_CHECKS = 0），导入完成后恢复

4. **字符编码**：确保 MySQL 连接使用 UTF-8 编码
   ```sql
   SET NAMES utf8mb4;
   ```

5. **数据验证**：导入后会自动执行验证查询，检查数据量和样例数据

## 常见问题

### Q1: 导入时报错 "Unknown database 'dormbill'"
**A**: 先创建数据库
```sql
CREATE DATABASE dormbill CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Q2: 报错 "Table 'buildings' doesn't exist"
**A**: 先运行数据库迁移
```bash
cd backend
alembic upgrade head
```

### Q3: 导入后员工或房间对不上
**A**: 检查 Excel 数据的姓名、楼号、房号、室号是否有空格或特殊字符

### Q4: 想只导入部分数据
**A**: 可以编辑 `import_all_data.sql`，注释掉不需要的部分：
```sql
-- 注释掉不需要的部分
-- TRUNCATE TABLE employees;
```

### Q5: 重复执行脚本会怎样
**A**: 每次执行都会清空数据并重新导入，不会产生重复数据

## 数据更新流程

如果 Excel 数据有更新：

1. 更新 `data/房间和人员数据.xlsx`
2. 重新生成 SQL：`python generate_import_sql.py`
3. 备份当前数据库（可选）
4. 执行新的 SQL 脚本

## 扩展功能

### 自定义入住日期

如需为不同员工设置不同的入住日期，可以在生成后手动修改 SQL 中的：

```sql
'2024-01-01' AS check_in_date,
```

### 添加电表信息

如需关联电表，可在导入后执行：

```sql
UPDATE rooms 
SET meter_no = '电表编号' 
WHERE building_id = X AND room_no = 'Y';
```

## 技术支持

如有问题，请查看：
- 项目根目录的 `README.md`
- 后端 API 文档
- 数据库 Schema 文档

---

**生成时间**: 2026-09-12  
**脚本版本**: v1.0  
**维护人员**: 开发团队
