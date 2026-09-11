-- 导入入住记录 - 完整版（处理合并单元格）
-- 生成时间: 2026-09-11
-- 数据来源: 7月宿舍员工 扣款.xlsx

INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '247')
WHERE e.name = '周可才'
  AND e.company = '天泽'
  AND r.room_no = '201'
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
    '夫妻间',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '247')
WHERE e.name = '熊青伟'
  AND e.company = '天泽'
  AND r.room_no = '201'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '247')
WHERE e.name = '宫凤云'
  AND e.company = '天泽'
  AND r.room_no = '201'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '247')
WHERE e.name = '刘磊'
  AND e.company = '天泽'
  AND r.room_no = '201'
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
    '7/1 入住，前3个月不收租',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '247')
WHERE e.name = '杨俊杰'
  AND e.company = '天檀'
  AND r.room_no = '201'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '247')
WHERE e.name = '周红军'
  AND e.company = '天泽'
  AND r.room_no = '201'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '247')
WHERE e.name = '冯敏'
  AND e.company = '天泽'
  AND r.room_no = '201'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '247')
WHERE e.name = '朱竹青'
  AND e.company = '天泽'
  AND r.room_no = '201'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '247')
WHERE e.name = '孙闯营'
  AND e.company = '天檀'
  AND r.room_no = '202'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '247')
WHERE e.name = '陈强'
  AND e.company = '天泽'
  AND r.room_no = '202'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '247')
WHERE e.name = '黄志雄'
  AND e.company = '天泽'
  AND r.room_no = '202'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '247')
WHERE e.name = '李运运'
  AND e.company = '芜湖'
  AND r.room_no = '202'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '247')
WHERE e.name = '肖仁华'
  AND e.company = '天泽'
  AND r.room_no = '202'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '248')
WHERE e.name = '宋显迪'
  AND e.company = '天泽'
  AND r.room_no = '301'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '248')
WHERE e.name = '林权'
  AND e.company = '天泽'
  AND r.room_no = '301'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '248')
WHERE e.name = '李东胜'
  AND e.company = '天泽'
  AND r.room_no = '301'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '248')
WHERE e.name = '李克宝'
  AND e.company = '天泽'
  AND r.room_no = '301'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '248')
WHERE e.name = '程龙浩'
  AND e.company = '天泽'
  AND r.room_no = '301'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '248')
WHERE e.name = '欧永波'
  AND e.company = '天泽'
  AND r.room_no = '301'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '248')
WHERE e.name = '孙涛'
  AND e.company = '天泽'
  AND r.room_no = '301'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '248')
WHERE e.name = '李中铭'
  AND e.company = '天泽'
  AND r.room_no = '302'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '248')
WHERE e.name = '杨宇'
  AND e.company = '天泽'
  AND r.room_no = '302'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '248')
WHERE e.name = '陈渝'
  AND e.company = '天泽'
  AND r.room_no = '302'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '248')
WHERE e.name = '董邦超'
  AND e.company = '天泽'
  AND r.room_no = '302'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '248')
WHERE e.name = '闵晓康'
  AND e.company = '天泽'
  AND r.room_no = '302'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '248')
WHERE e.name = '钱纪'
  AND e.company = '天泽'
  AND r.room_no = '302'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '248')
WHERE e.name = '汪文杰'
  AND e.company = '天泽'
  AND r.room_no = '302'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '248')
WHERE e.name = '陈少华'
  AND e.company = '天泽'
  AND r.room_no = '402'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '248')
WHERE e.name = '袁世梁'
  AND e.company = '天泽'
  AND r.room_no = '402'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '248')
WHERE e.name = '邓涛'
  AND e.company = '天泽'
  AND r.room_no = '402'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '248')
WHERE e.name = '李华丹'
  AND e.company = '天泽'
  AND r.room_no = '402'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '248')
WHERE e.name = '张月东'
  AND e.company = '天泽'
  AND r.room_no = '402'
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
    '夫妻间',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '248')
WHERE e.name = '王德凯'
  AND e.company = '天泽'
  AND r.room_no = '402'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '248')
WHERE e.name = '梁凤'
  AND e.company = '天泽'
  AND r.room_no = '402'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '249')
WHERE e.name = '张聪'
  AND e.company = '天檀'
  AND r.room_no = '201'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '249')
WHERE e.name = '邹建'
  AND e.company = '天泽'
  AND r.room_no = '201'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '249')
WHERE e.name = '钱瑞蕾'
  AND e.company = '天檀'
  AND r.room_no = '301'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '249')
WHERE e.name = '殷陈陈'
  AND e.company = '天泽'
  AND r.room_no = '301'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '249')
WHERE e.name = '朱宇豪'
  AND e.company = '天泽'
  AND r.room_no = '301'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '249')
WHERE e.name = '熊正娣'
  AND e.company = '天泽'
  AND r.room_no = '301'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '249')
WHERE e.name = '陈碧峰'
  AND e.company = '天泽'
  AND r.room_no = '301'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '249')
WHERE e.name = '罗雄'
  AND e.company = '天檀'
  AND r.room_no = '301'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '249')
WHERE e.name = '张甲坤'
  AND e.company = '天檀'
  AND r.room_no = '301'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '249')
WHERE e.name = '李成鹏'
  AND e.company = '天泽'
  AND r.room_no = '302'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '249')
WHERE e.name = '方奇锋'
  AND e.company = '天泽'
  AND r.room_no = '302'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '249')
WHERE e.name = '陈顺新'
  AND e.company = '天泽'
  AND r.room_no = '302'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '249')
WHERE e.name = '陶冲'
  AND e.company = '天檀'
  AND r.room_no = '302'
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
    '4/20 入住前三个月不收租',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '249')
WHERE e.name = '黄浩然'
  AND e.company = '天泽'
  AND r.room_no = '302'
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
    '7/9 转宿到99弄46号',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '249')
WHERE e.name = '郭雅格'
  AND e.company = '天泽'
  AND r.room_no = '302'
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
    '暑假工',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '249')
WHERE e.name = '石昌东'
  AND e.company = ''
  AND r.room_no = '302'
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
    '暑假工',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '249')
WHERE e.name = '石永胜'
  AND e.company = ''
  AND r.room_no = '302'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '249')
WHERE e.name = '李加明'
  AND e.company = '天泽'
  AND r.room_no = '302'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '249')
WHERE e.name = '唐历'
  AND e.company = '天泽'
  AND r.room_no = '401'
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
    '7/15 入住',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '249')
WHERE e.name = '张志胜'
  AND e.company = '天泽'
  AND r.room_no = '401'
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
    '7/9 入住前三个月不收租',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '249')
WHERE e.name = '乔亚冬'
  AND e.company = '天泽'
  AND r.room_no = '401'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '249')
WHERE e.name = '朱国甫'
  AND e.company = '天泽'
  AND r.room_no = '401'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '249')
WHERE e.name = '冯金平'
  AND e.company = '天檀'
  AND r.room_no = '401'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '249')
WHERE e.name = '孙彦超'
  AND e.company = '天檀'
  AND r.room_no = '401'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '249')
WHERE e.name = '颜红良'
  AND e.company = '天泽'
  AND r.room_no = '401'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '249')
WHERE e.name = '姚贵川'
  AND e.company = '天泽'
  AND r.room_no = '401'
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
    '7/1 搬入',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '249')
WHERE e.name = '尹杰'
  AND e.company = '天泽'
  AND r.room_no = '402'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '249')
WHERE e.name = '范椿泉'
  AND e.company = '天泽'
  AND r.room_no = '402'
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
    '独自拉了一个大床，有家属',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '249')
WHERE e.name = '汪永进'
  AND e.company = '天泽'
  AND r.room_no = '402'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '249')
WHERE e.name = '赵俊毫'
  AND e.company = '天檀'
  AND r.room_no = '402'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '249')
WHERE e.name = '邓亭'
  AND e.company = '天泽'
  AND r.room_no = '402'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '249')
WHERE e.name = '朱时雨'
  AND e.company = '天泽'
  AND r.room_no = '402'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '249')
WHERE e.name = '仲生荣'
  AND e.company = '天泽'
  AND r.room_no = '402'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '胡磊磊'
  AND e.company = '天泽'
  AND r.room_no = '301'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '吕立永(夜班）'
  AND e.company = '天泽'
  AND r.room_no = '301'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '谢之兴'
  AND e.company = '天泽'
  AND r.room_no = '301'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '林三添'
  AND e.company = '天檀'
  AND r.room_no = '301'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '孙波'
  AND e.company = '天泽'
  AND r.room_no = '301'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '王鑫'
  AND e.company = '天泽'
  AND r.room_no = '301'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '王浩然'
  AND e.company = '天泽'
  AND r.room_no = '301'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '单振荡'
  AND e.company = '天泽'
  AND r.room_no = '301'
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
    NULL,
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '童朝海'
  AND e.company = '天泽'
  AND r.room_no = '301'
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
    '7.27—8.15  水电租全免',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '毛志令'
  AND e.company = '芜湖'
  AND r.room_no = '302'
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
    '每次住半个月，水电租全免',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '赵蒙凯'
  AND e.company = '芜湖'
  AND r.room_no = '302'
  AND r.room_unit = '2'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;

-- 跳过: 雷寿燕 (天泽) - 房间格式错误: 250-401（女生宿舍）-1.0
-- 跳过: 洪学琴 (天泽) - 房间格式错误: 250-401（女生宿舍）-2.0
-- 跳过: 潘珏 (天檀) - 房间格式错误: 250-401（女生宿舍）-2.0
-- 跳过: 刘佳慧 (天泽) - 房间格式错误: 250-401（女生宿舍）-3.0
-- 跳过: 江歙凤 (天泽) - 房间格式错误: 250-401（女生宿舍）-4.0
-- 跳过: 孙俊 (天泽) - 房间格式错误: 250-402（女生宿舍）-1.0
-- 跳过: 陈倩倩 () - 房间格式错误: 250-402（女生宿舍）-2.0
-- 跳过: 冯晶琳 (天泽) - 房间格式错误: 250-402（女生宿舍）-3.0
-- 跳过: 尚歆舒 (天泽) - 房间格式错误: 250-402（女生宿舍）-3.0
-- 跳过: 刁万瑞 () - 房间格式错误: 250-402（女生宿舍）-4.0
-- 跳过: 边艳艳 () - 房间格式错误: 250-402（女生宿舍）-4.0
-- 跳过: 羊蔚琛 (天泽) - 房间格式错误: 250-402（女生宿舍）-5.0
-- 跳过: 罗国庆 (天泽) - 房间格式错误: 99-83-402（女生宿舍）-1.0
-- 跳过: 黄明 (拓施培) - 房间格式错误: 99-83-402（女生宿舍）-2.0
-- 跳过: 范成杰 (天泽) - 房间格式错误: 99-83-402（女生宿舍）-3.0
-- 跳过: 何海洋 (拓施培) - 房间格式错误: 99-83-402（女生宿舍）-3.0
-- 跳过: 于乐乐 (天泽) - 房间格式错误: 99-83-402（女生宿舍）-4.0
-- 跳过: 李兴海 (天泽) - 房间格式错误: 99-83-402（女生宿舍）-4.0
-- 跳过: 杨城 (拓施培) - 房间格式错误: 99-83-402（女生宿舍）-5.0
-- 跳过: 包康 (拓施培) - 房间格式错误: 99-83-402（女生宿舍）-5.0
-- 跳过: 周艳龙 (天泽) - 房间格式错误: 99-84-402（女生宿舍）-1.0
-- 跳过: 陈清水 (天泽) - 房间格式错误: 99-84-402（女生宿舍）-2.0
-- 跳过: 茹金才 (天泽) - 房间格式错误: 99-84-402（女生宿舍）-3.0
-- 跳过: 翟飞龙 (天泽) - 房间格式错误: 99-84-402（女生宿舍）-4.0
-- 跳过: 张英华 (天泽) - 房间格式错误: 99-84-402（女生宿舍）-5.0
-- 跳过: 姚新奥 (拓施培) - 房间格式错误: 99-45-402（女生宿舍）-1.0
-- 跳过: 方子健 (天泽) - 房间格式错误: 99-45-402（女生宿舍）-1.0
-- 跳过: 李家伟 (天檀) - 房间格式错误: 99-45-402（女生宿舍）-2.0
-- 跳过: 马翔翔 (天檀) - 房间格式错误: 99-45-402（女生宿舍）-2.0
-- 跳过: 蔡第强 (天泽) - 房间格式错误: 99-45-402（女生宿舍）-3.0
-- 跳过: 张鹏超 (天泽) - 房间格式错误: 99-45-402（女生宿舍）-3.0
-- 跳过: 洛绒生龙 (天泽) - 房间格式错误: 99-45-402（女生宿舍）-4.0
-- 跳过: 郭红阳 (天泽) - 房间格式错误: 99-45-402（女生宿舍）-5.0
-- 跳过: 李致远 (拓施培) - 房间格式错误: 99-45-402（女生宿舍）-5.0
-- 跳过: 莫红震 (天泽) - 房间格式错误: 99-46-402（女生宿舍）-1.0
-- 跳过: 李飞建 () - 房间格式错误: 99-46-402（女生宿舍）-1.0
-- 跳过: 孙晨朔 (拓施培) - 房间格式错误: 99-46-402（女生宿舍）-2.0
-- 跳过: 刘旭 (天泽) - 房间格式错误: 99-46-402（女生宿舍）-2.0
-- 跳过: 秦孝红 (拓施培) - 房间格式错误: 99-46-402（女生宿舍）-3.0
-- 跳过: 薛健华 (拓施培) - 房间格式错误: 99-46-402（女生宿舍）-3.0
-- 跳过: 庄荣飞 (拓施培) - 房间格式错误: 99-46-402（女生宿舍）-4.0
-- 跳过: 郭雅格 (天泽) - 房间格式错误: 99-46-402（女生宿舍）-4.0
-- 跳过: 雷志飞 (天泽) - 房间格式错误: 99-46-402（女生宿舍）-5.0
-- 跳过: 孙洪力 (天泽) - 房间格式错误: 99-46-402（女生宿舍）-5.0