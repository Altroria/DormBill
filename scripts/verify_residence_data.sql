-- 验证入住记录数据

-- 1. 按公司统计入住人数
SELECT '按公司统计' AS 类型, '' AS 详情;
SELECT 
    e.company AS 公司,
    COUNT(*) AS 入住人数
FROM residence_records rr
JOIN employees e ON rr.employee_id = e.id
GROUP BY e.company
ORDER BY COUNT(*) DESC;

-- 2. 按楼栋统计入住情况
SELECT '按楼栋统计' AS 类型, '' AS 详情;
SELECT 
    b.building_no AS 楼号,
    COUNT(DISTINCT rr.room_id) AS 入住房间数,
    COUNT(*) AS 入住人数
FROM residence_records rr
JOIN rooms r ON rr.room_id = r.id
JOIN buildings b ON r.building_id = b.id
GROUP BY b.building_no
ORDER BY b.building_no;

-- 3. 查看前20条入住记录
SELECT '入住记录样本（前20条）' AS 类型, '' AS 详情;
SELECT 
    e.name AS 员工姓名,
    e.company AS 公司,
    CONCAT(b.building_no, '-', r.room_no, '-', r.room_unit) AS 完整房间号,
    r.room_name AS 房间名称,
    rr.check_in_date AS 入住日期,
    rr.remark AS 备注
FROM residence_records rr
JOIN employees e ON rr.employee_id = e.id
JOIN rooms r ON rr.room_id = r.id
JOIN buildings b ON r.building_id = b.id
ORDER BY b.building_no, r.room_no, r.room_unit
LIMIT 20;

-- 4. 检查Excel中有但数据库中缺失的员工（基于公司统计）
SELECT '数据对比分析' AS 类型, '' AS 详情;
SELECT 
    'Excel总记录' AS 项目,
    '122' AS 数量,
    '来源：7月宿舍员工 扣款.xlsx' AS 说明
UNION ALL
SELECT 
    '数据库记录' AS 项目,
    CAST(COUNT(*) AS CHAR) AS 数量,
    '当前residence_records表' AS 说明
FROM residence_records
UNION ALL
SELECT 
    '差异' AS 项目,
    CAST((122 - COUNT(*)) AS CHAR) AS 数量,
    '需要处理的记录（主要是女生宿舍特殊格式）' AS 说明
FROM residence_records;
