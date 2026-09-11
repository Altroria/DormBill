-- 诊断女生宿舍导入失败原因

-- 1. 检查250楼是否存在
SELECT '检查250楼' AS 检查项;
SELECT * FROM buildings WHERE building_no = '250';

-- 2. 检查250楼的房间
SELECT '检查250楼的房间' AS 检查项;
SELECT 
    r.id,
    b.building_no,
    r.room_no,
    r.room_unit,
    r.room_name
FROM rooms r
JOIN buildings b ON r.building_id = b.id
WHERE b.building_no = '250'
ORDER BY r.room_no, r.room_unit;

-- 3. 检查女生宿舍相关员工
SELECT '检查雷寿燕等员工' AS 检查项;
SELECT id, name, company FROM employees 
WHERE name IN ('雷寿燕', '洪学琴', '潘珏', '刘佳慧', '江歙凤')
ORDER BY company, name;

-- 4. 测试单条插入 - 雷寿燕
SELECT '测试雷寿燕匹配情况' AS 检查项;
SELECT 
    e.id AS employee_id,
    e.name,
    e.company,
    r.id AS room_id,
    CONCAT(b.building_no, '-', r.room_no, '-', r.room_unit) AS room_full,
    r.room_name
FROM employees e
CROSS JOIN rooms r
JOIN buildings b ON r.building_id = b.id
WHERE e.name = '雷寿燕'
  AND e.company = '天泽'
  AND b.building_no = '250'
  AND r.room_no = '401';

-- 5. 检查室号类型
SELECT '检查401室的所有室号' AS 检查项;
SELECT 
    r.room_unit,
    TYPEOF(r.room_unit) AS unit_type,
    LENGTH(r.room_unit) AS unit_length
FROM rooms r
JOIN buildings b ON r.building_id = b.id
WHERE b.building_no = '250' AND r.room_no = '401';
