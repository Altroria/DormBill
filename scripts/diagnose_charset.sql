-- 诊断数据库字符集配置
-- 运行日期: 2026-09-11

-- 1. 检查数据库字符集
SHOW VARIABLES LIKE 'character_set%';
SHOW VARIABLES LIKE 'collation%';

-- 2. 检查数据库级别的字符集
SELECT 
    SCHEMA_NAME,
    DEFAULT_CHARACTER_SET_NAME,
    DEFAULT_COLLATION_NAME
FROM information_schema.SCHEMATA
WHERE SCHEMA_NAME = 'dormbill';

-- 3. 检查各表的字符集
SELECT 
    TABLE_NAME, 
    TABLE_COLLATION
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = 'dormbill'
ORDER BY TABLE_NAME;

-- 4. 检查各表字段的字符集
SELECT 
    TABLE_NAME,
    COLUMN_NAME,
    CHARACTER_SET_NAME,
    COLLATION_NAME,
    COLUMN_TYPE
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = 'dormbill'
    AND CHARACTER_SET_NAME IS NOT NULL
ORDER BY TABLE_NAME, ORDINAL_POSITION;

-- 5. 查看示例数据（检查是否乱码）
SELECT '=== Buildings ===' as section;
SELECT id, building_no, name, HEX(name) as name_hex FROM buildings LIMIT 3;

SELECT '=== Rooms ===' as section;
SELECT id, room_no, room_name, HEX(room_name) as room_name_hex FROM rooms LIMIT 5;

SELECT '=== Employees ===' as section;
SELECT id, name, HEX(name) as name_hex, company FROM employees LIMIT 5;
