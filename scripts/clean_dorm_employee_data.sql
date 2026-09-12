-- ============================================================
-- 宿舍与员工相关表清空脚本
-- 适用: dormbill 数据库
-- 说明: 仅清空宿舍管理 + 员工管理相关表(buildings/rooms/
--       employees/residence_records),其它业务表(电表/水表/
--       结算/操作日志等)不受影响
-- 使用: mysql -uroot -p[dormbill] < clean_dorm_employee_data.sql
-- ============================================================

-- 字符集
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
SET COLLATION_CONNECTION = 'utf8mb4_unicode_ci';

-- 关闭外键,避免被依赖顺序阻断
SET FOREIGN_KEY_CHECKS = 0;

-- 开始事务,出错可回滚
START TRANSACTION;

-- 1) 入住记录(子表,先清)
TRUNCATE TABLE residence_records;

-- 2) 房间
TRUNCATE TABLE rooms;

-- 3) 员工
TRUNCATE TABLE employees;

-- 4) 楼栋
TRUNCATE TABLE buildings;

COMMIT;

-- 恢复外键检查
SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================
-- 校验:确认四张表已清空
-- ============================================================
SELECT
  (SELECT COUNT(*) FROM buildings)         AS buildings_count,
  (SELECT COUNT(*) FROM rooms)             AS rooms_count,
  (SELECT COUNT(*) FROM employees)         AS employees_count,
  (SELECT COUNT(*) FROM residence_records) AS residence_records_count;
