-- 修复数据库字符集问题
-- 运行日期: 2026-09-11

-- 1. 设置当前会话字符集
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- 2. 修改数据库默认字符集
ALTER DATABASE dormbill CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- 3. 修改各表的字符集
ALTER TABLE buildings CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE rooms CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE employees CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE residence_records CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE electricity_meters CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE water_meters CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE settlements CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE operation_logs CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 4. 验证字符集设置
SELECT 
    TABLE_NAME, 
    TABLE_COLLATION,
    CHARACTER_SET_NAME
FROM information_schema.TABLES t
JOIN information_schema.COLLATION_CHARACTER_SET_APPLICABILITY ccsa 
    ON t.TABLE_COLLATION = ccsa.COLLATION_NAME
WHERE TABLE_SCHEMA = 'dormbill'
ORDER BY TABLE_NAME;

-- 5. 查看示例数据（验证中文是否正常）
SELECT id, building_no, name FROM buildings LIMIT 5;
SELECT id, room_no, room_name FROM rooms WHERE room_name LIKE '%单间%' LIMIT 5;
SELECT id, name, company FROM employees LIMIT 5;
