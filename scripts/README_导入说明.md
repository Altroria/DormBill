# 宿舍 & 员工 数据导入说明

## 文件清单

| 文件 | 作用 |
|---|---|
| `scripts/clean_dorm_employee_data.sql` | 仅清空宿舍/员工相关 4 张表(其它业务表不受影响) |
| `scripts/generate_dorm_employee_import_sql.py` | 从 `房间和人员数据.xlsx` 生成导入 SQL |
| `scripts/import_dorm_employee_from_xlsx.sql` | 由上述脚本生成的最终 SQL(可执行) |

## 涉及表

- `buildings` — 楼栋
- `rooms` — 房间(按 楼栋+房号+室号+房间名称 唯一)
- `employees` — 员工
- `residence_records` — 入住记录

**不涉及的表**: `meter_records`、`water_expenses`、`settlements`、`operation_logs`、`meter_readings` 等业务表保持原样。

## 使用步骤

> ⚠️ 清空是破坏性操作,执行前请确认已备份数据库

```bash
# 1) (可选)备份
docker compose -f docker-compose.prod.yml exec mysql \
  mysqldump -uroot -p --default-character-set=utf8mb4 \
  dormbill buildings rooms employees residence_records \
  > backup_dorm_employee_$(date +%Y%m%d_%H%M%S).sql

# 2) 清空 4 张表
docker compose -f docker-compose.prod.yml exec mysql \
  mysql -uroot -p --default-character-set=utf8mb4 dormbill \
  < scripts/clean_dorm_employee_data.sql

# 3) 生成导入 SQL(如果改了 Excel,先跑这一步重生 SQL)
python scripts/generate_dorm_employee_import_sql.py

# 4) 执行导入
docker compose -f docker-compose.prod.yml exec mysql \
  mysql -uroot -p --default-character-set=utf8mb4 dormbill \
  < scripts/import_dorm_employee_from_xlsx.sql
```

## 数据解析规则

### Excel 列映射
| Excel 列 | 数据库字段 |
|---|---|
| 楼号 | `buildings.building_no` |
| 房号 | `rooms.room_no` |
| 室号 | `rooms.room_unit` |
| 房间 | `rooms.room_name` |
| 房租(首个非零) | `rooms.rent_standard` |
| 任职单位 | `employees.company` |
| 一级部门 | `employees.department` |
| 职务 | `employees.position` |
| 姓名 | `employees.name` |
| 转宿日期 | `residence_records.check_in_date` |
| 房租 | `residence_records.remark` (作为 月租:N 备注) |

### 特殊规则

1. **合并单元格**: 沿用上一行的楼号/房号
2. **空房间**: 没有姓名的行只创建房间,不创建员工和入住记录
3. **入住日期**:
   - 备注里出现 `M/D` 形式 → 解析为 `M月D日`,年取当前年(2026)
   - 备注里出现 `入住`/`搬入` 关键字 → 作为 `check_in_date`
   - 否则默认 = 当月 1 日
4. **搬离/转宿**: 备注里出现 `离宿`/`转宿`/`搬出`/`搬离`/`退租` 关键字
   - `check_out_date` = 解析出的日期
   - `status` = `invalid`
   - `check_in_date` = 当月 1 日(原入住日未知,默认值)
5. **暑假工/未填写单位**: `company='未知'`,`department`/`position` 为 `NULL`
6. **夫妻间**: `is_primary_payer=1`(识别关键字:备注里含 `夫妻间`)

## 本次导入结果

```
楼栋:     5 个   (247 / 248 / 249 / 250 / 99)
房间:    98 个
员工:   121 个
入住记录: 122 条 (其中 3 条 status='invalid' 为已搬离/转宿)
```
