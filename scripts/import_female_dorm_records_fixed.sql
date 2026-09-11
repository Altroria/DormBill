-- 女生宿舍入住记录导入（修复版）
-- 生成时间: 2026-09-11 11:14:16
-- 修复点：
-- 1. 室号格式：1.0 -> 1
-- 2. 房间号匹配：使用LIKE '401%'匹配'401（女生宿舍）'


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '雷寿燕'
  AND e.company = '天泽'
  AND r.room_no LIKE '401%'
  AND r.room_unit = '1'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '洪学琴'
  AND e.company = '天泽'
  AND r.room_no LIKE '401%'
  AND r.room_unit = '2'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '潘珏'
  AND e.company = '天檀'
  AND r.room_no LIKE '401%'
  AND r.room_unit = '2'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '刘佳慧 '
  AND e.company = '天泽'
  AND r.room_no LIKE '401%'
  AND r.room_unit = '3'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '江歙凤'
  AND e.company = '天泽'
  AND r.room_no LIKE '401%'
  AND r.room_unit = '4'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '孙俊'
  AND e.company = '天泽'
  AND r.room_no LIKE '402%'
  AND r.room_unit = '1'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '陈倩倩'
  AND e.company = '未知'
  AND r.room_no LIKE '402%'
  AND r.room_unit = '2'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '冯晶琳'
  AND e.company = '天泽'
  AND r.room_no LIKE '402%'
  AND r.room_unit = '3'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '尚歆舒'
  AND e.company = '天泽'
  AND r.room_no LIKE '402%'
  AND r.room_unit = '3'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '刁万瑞'
  AND e.company = '未知'
  AND r.room_no LIKE '402%'
  AND r.room_unit = '4'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '边艳艳'
  AND e.company = '未知'
  AND r.room_no LIKE '402%'
  AND r.room_unit = '4'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '羊蔚琛'
  AND e.company = '天泽'
  AND r.room_no LIKE '402%'
  AND r.room_unit = '5'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '罗国庆'
  AND e.company = '天泽'
  AND r.room_no LIKE '402%'
  AND r.room_unit = '1'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '黄明'
  AND e.company = '拓施培'
  AND r.room_no LIKE '402%'
  AND r.room_unit = '2'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '范成杰'
  AND e.company = '天泽'
  AND r.room_no LIKE '402%'
  AND r.room_unit = '3'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '何海洋'
  AND e.company = '拓施培'
  AND r.room_no LIKE '402%'
  AND r.room_unit = '3'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '于乐乐'
  AND e.company = '天泽'
  AND r.room_no LIKE '402%'
  AND r.room_unit = '4'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '李兴海'
  AND e.company = '天泽'
  AND r.room_no LIKE '402%'
  AND r.room_unit = '4'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '杨城'
  AND e.company = '拓施培'
  AND r.room_no LIKE '402%'
  AND r.room_unit = '5'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '包康'
  AND e.company = '拓施培'
  AND r.room_no LIKE '402%'
  AND r.room_unit = '5'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '周艳龙'
  AND e.company = '天泽'
  AND r.room_no LIKE '402%'
  AND r.room_unit = '1'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '陈清水'
  AND e.company = '天泽'
  AND r.room_no LIKE '402%'
  AND r.room_unit = '2'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '茹金才'
  AND e.company = '天泽'
  AND r.room_no LIKE '402%'
  AND r.room_unit = '3'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '翟飞龙'
  AND e.company = '天泽'
  AND r.room_no LIKE '402%'
  AND r.room_unit = '4'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '张英华'
  AND e.company = '天泽'
  AND r.room_no LIKE '402%'
  AND r.room_unit = '5'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '姚新奥'
  AND e.company = '拓施培'
  AND r.room_no LIKE '402%'
  AND r.room_unit = '1'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '方子健'
  AND e.company = '天泽'
  AND r.room_no LIKE '402%'
  AND r.room_unit = '1'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '李家伟'
  AND e.company = '天檀'
  AND r.room_no LIKE '402%'
  AND r.room_unit = '2'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '马翔翔'
  AND e.company = '天檀'
  AND r.room_no LIKE '402%'
  AND r.room_unit = '2'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '蔡第强'
  AND e.company = '天泽'
  AND r.room_no LIKE '402%'
  AND r.room_unit = '3'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '张鹏超'
  AND e.company = '天泽'
  AND r.room_no LIKE '402%'
  AND r.room_unit = '3'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '洛绒生龙'
  AND e.company = '天泽'
  AND r.room_no LIKE '402%'
  AND r.room_unit = '4'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '郭红阳'
  AND e.company = '天泽'
  AND r.room_no LIKE '402%'
  AND r.room_unit = '5'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '李致远'
  AND e.company = '拓施培'
  AND r.room_no LIKE '402%'
  AND r.room_unit = '5'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '莫红震'
  AND e.company = '天泽'
  AND r.room_no LIKE '402%'
  AND r.room_unit = '1'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '李飞建'
  AND e.company = '未知'
  AND r.room_no LIKE '402%'
  AND r.room_unit = '1'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '孙晨朔'
  AND e.company = '拓施培'
  AND r.room_no LIKE '402%'
  AND r.room_unit = '2'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '刘旭'
  AND e.company = '天泽'
  AND r.room_no LIKE '402%'
  AND r.room_unit = '2'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '秦孝红'
  AND e.company = '拓施培'
  AND r.room_no LIKE '402%'
  AND r.room_unit = '3'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '薛健华'
  AND e.company = '拓施培'
  AND r.room_no LIKE '402%'
  AND r.room_unit = '3'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '庄荣飞'
  AND e.company = '拓施培'
  AND r.room_no LIKE '402%'
  AND r.room_unit = '4'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '郭雅格'
  AND e.company = '天泽'
  AND r.room_no LIKE '402%'
  AND r.room_unit = '4'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '雷志飞'
  AND e.company = '天泽'
  AND r.room_no LIKE '402%'
  AND r.room_unit = '5'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;


INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '孙洪力'
  AND e.company = '天泽'
  AND r.room_no LIKE '402%'
  AND r.room_unit = '5'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;
