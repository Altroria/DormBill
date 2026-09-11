-- 检查入住记录缺失数据
-- 生成时间: 2026-09-11

-- 1. 统计当前入住记录
SELECT '当前入住记录统计' as 检查项;
SELECT 
  COUNT(*) as 总记录数,
  COUNT(DISTINCT employee_id) as 员工数,
  COUNT(DISTINCT room_id) as 房间数
FROM residence_records;

-- 2. 按楼栋统计
SELECT '按楼栋统计入住情况' as 检查项;
SELECT 
  b.building_no AS 楼号,
  COUNT(DISTINCT r.id) as 房间总数,
  COUNT(DISTINCT rr.room_id) as 已入住房间数,
  COUNT(rr.id) as 入住人数
FROM buildings b
LEFT JOIN rooms r ON r.building_id = b.id
LEFT JOIN residence_records rr ON rr.room_id = r.id
GROUP BY b.building_no
ORDER BY b.building_no;

-- 3. 查找未入住的房间
SELECT '未入住的房间' as 检查项;
SELECT 
  b.building_no AS 楼号,
  r.room_no AS 房号,
  r.room_unit AS 室号,
  r.room_name AS 房间名称,
  r.status AS 状态
FROM rooms r
JOIN buildings b ON r.building_id = b.id
LEFT JOIN residence_records rr ON rr.room_id = r.id
WHERE rr.id IS NULL AND r.status = 'available'
ORDER BY b.building_no, r.room_no, r.room_unit;

-- 4. 查找未分配房间的员工
SELECT '未分配房间的员工' as 检查项;
SELECT 
  e.name AS 姓名,
  e.company AS 公司,
  e.department AS 部门,
  e.position AS 职位
FROM employees e
LEFT JOIN residence_records rr ON rr.employee_id = e.id
WHERE rr.id IS NULL AND e.status = 'active'
ORDER BY e.company, e.name
LIMIT 50;

-- 5. 查看最近导入的记录
SELECT '最近导入的10条记录' as 检查项;
SELECT 
  e.name AS 员工,
  e.company AS 公司,
  CONCAT(b.building_no, '-', r.room_no, '-', r.room_unit) AS 房间,
  r.room_name AS 房间名称,
  rr.check_in_date AS 入住日期,
  rr.remark AS 备注
FROM residence_records rr
JOIN employees e ON rr.employee_id = e.id
JOIN rooms r ON rr.room_id = r.id
JOIN buildings b ON r.building_id = b.id
ORDER BY rr.id DESC
LIMIT 10;
