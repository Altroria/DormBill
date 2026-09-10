-- 房间数据导入SQL
-- 此SQL会先尝试更新，如果房间不存在则插入新记录

-- 设置字符集
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- 247-201-1
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '201', '1', '北小单间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '247'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '201' AND r2.room_unit = '1'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '北小单间'
WHERE b.building_no = '247' AND r.room_no = '201' AND r.room_unit = '1';

-- 247-201-2
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '201', '2', '南隔间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '247'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '201' AND r2.room_unit = '2'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南隔间'
WHERE b.building_no = '247' AND r.room_no = '201' AND r.room_unit = '2';

-- 247-201-3
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '201', '3', '南带飘窗间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '247'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '201' AND r2.room_unit = '3'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南带飘窗间'
WHERE b.building_no = '247' AND r.room_no = '201' AND r.room_unit = '3';

-- 247-201-4
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '201', '4', '南独卫', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '247'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '201' AND r2.room_unit = '4'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南独卫'
WHERE b.building_no = '247' AND r.room_no = '201' AND r.room_unit = '4';

-- 247-202-1
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '202', '1', '南独卫', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '247'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '202' AND r2.room_unit = '1'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南独卫'
WHERE b.building_no = '247' AND r.room_no = '202' AND r.room_unit = '1';

-- 247-202-2
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '202', '2', '北小单间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '247'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '202' AND r2.room_unit = '2'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '北小单间'
WHERE b.building_no = '247' AND r.room_no = '202' AND r.room_unit = '2';

-- 247-202-3
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '202', '3', '南隔间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '247'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '202' AND r2.room_unit = '3'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南隔间'
WHERE b.building_no = '247' AND r.room_no = '202' AND r.room_unit = '3';

-- 247-202-4
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '202', '4', '南带飘窗间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '247'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '202' AND r2.room_unit = '4'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南带飘窗间'
WHERE b.building_no = '247' AND r.room_no = '202' AND r.room_unit = '4';

-- 248-301-1
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '301', '1', '北厨房隔间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '248'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '301' AND r2.room_unit = '1'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '北厨房隔间'
WHERE b.building_no = '248' AND r.room_no = '301' AND r.room_unit = '1';

-- 248-301-2
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '301', '2', '北小单间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '248'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '301' AND r2.room_unit = '2'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '北小单间'
WHERE b.building_no = '248' AND r.room_no = '301' AND r.room_unit = '2';

-- 248-301-3
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '301', '3', '南客隔间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '248'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '301' AND r2.room_unit = '3'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南客隔间'
WHERE b.building_no = '248' AND r.room_no = '301' AND r.room_unit = '3';

-- 248-301-4
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '301', '4', '南带飘窗间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '248'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '301' AND r2.room_unit = '4'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南带飘窗间'
WHERE b.building_no = '248' AND r.room_no = '301' AND r.room_unit = '4';

-- 248-301-5
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '301', '5', '南独卫', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '248'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '301' AND r2.room_unit = '5'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南独卫'
WHERE b.building_no = '248' AND r.room_no = '301' AND r.room_unit = '5';

-- 248-302-1
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '302', '1', '北厨房隔间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '248'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '302' AND r2.room_unit = '1'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '北厨房隔间'
WHERE b.building_no = '248' AND r.room_no = '302' AND r.room_unit = '1';

-- 248-302-2
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '302', '2', '北小单间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '248'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '302' AND r2.room_unit = '2'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '北小单间'
WHERE b.building_no = '248' AND r.room_no = '302' AND r.room_unit = '2';

-- 248-302-3
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '302', '3', '南客隔间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '248'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '302' AND r2.room_unit = '3'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南客隔间'
WHERE b.building_no = '248' AND r.room_no = '302' AND r.room_unit = '3';

-- 248-302-4
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '302', '4', '南带飘窗间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '248'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '302' AND r2.room_unit = '4'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南带飘窗间'
WHERE b.building_no = '248' AND r.room_no = '302' AND r.room_unit = '4';

-- 248-302-5
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '302', '5', '南独卫', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '248'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '302' AND r2.room_unit = '5'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南独卫'
WHERE b.building_no = '248' AND r.room_no = '302' AND r.room_unit = '5';

-- 248-401-1
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '401', '1', '客改间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '248'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '401' AND r2.room_unit = '1'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '客改间'
WHERE b.building_no = '248' AND r.room_no = '401' AND r.room_unit = '1';

-- 248-401-2
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '401', '2', '南飘窗', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '248'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '401' AND r2.room_unit = '2'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南飘窗'
WHERE b.building_no = '248' AND r.room_no = '401' AND r.room_unit = '2';

-- 248-401-3
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '401', '3', '独立卫生间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '248'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '401' AND r2.room_unit = '3'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '独立卫生间'
WHERE b.building_no = '248' AND r.room_no = '401' AND r.room_unit = '3';

-- 248-401-4
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '401', '4', '北小单间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '248'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '401' AND r2.room_unit = '4'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '北小单间'
WHERE b.building_no = '248' AND r.room_no = '401' AND r.room_unit = '4';

-- 248-401-5
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '401', '5', '北厨改', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '248'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '401' AND r2.room_unit = '5'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '北厨改'
WHERE b.building_no = '248' AND r.room_no = '401' AND r.room_unit = '5';

-- 248-401-6
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '401', '6', '北厨改套间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '248'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '401' AND r2.room_unit = '6'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '北厨改套间'
WHERE b.building_no = '248' AND r.room_no = '401' AND r.room_unit = '6';

-- 248-402-1
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '402', '1', '北厨房隔间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '248'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '402' AND r2.room_unit = '1'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '北厨房隔间'
WHERE b.building_no = '248' AND r.room_no = '402' AND r.room_unit = '1';

-- 248-402-2
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '402', '2', '北小单间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '248'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '402' AND r2.room_unit = '2'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '北小单间'
WHERE b.building_no = '248' AND r.room_no = '402' AND r.room_unit = '2';

-- 248-402-3
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '402', '3', '南客隔间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '248'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '402' AND r2.room_unit = '3'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南客隔间'
WHERE b.building_no = '248' AND r.room_no = '402' AND r.room_unit = '3';

-- 248-402-4
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '402', '4', '南带飘窗间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '248'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '402' AND r2.room_unit = '4'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南带飘窗间'
WHERE b.building_no = '248' AND r.room_no = '402' AND r.room_unit = '4';

-- 248-402-5
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '402', '5', '南独卫', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '248'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '402' AND r2.room_unit = '5'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南独卫'
WHERE b.building_no = '248' AND r.room_no = '402' AND r.room_unit = '5';

-- 249-201-1
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '201', '1', '北厨房隔间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '249'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '201' AND r2.room_unit = '1'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '北厨房隔间'
WHERE b.building_no = '249' AND r.room_no = '201' AND r.room_unit = '1';

-- 249-201-2
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '201', '2', '', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '249'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '201' AND r2.room_unit = '2'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = ''
WHERE b.building_no = '249' AND r.room_no = '201' AND r.room_unit = '2';

-- 249-201-3
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '201', '3', '南独卫', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '249'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '201' AND r2.room_unit = '3'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南独卫'
WHERE b.building_no = '249' AND r.room_no = '201' AND r.room_unit = '3';

-- 249-301-1
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '301', '1', '北小单间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '249'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '301' AND r2.room_unit = '1'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '北小单间'
WHERE b.building_no = '249' AND r.room_no = '301' AND r.room_unit = '1';

-- 249-301-2
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '301', '2', '北厨房隔间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '249'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '301' AND r2.room_unit = '2'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '北厨房隔间'
WHERE b.building_no = '249' AND r.room_no = '301' AND r.room_unit = '2';

-- 249-301-3
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '301', '3', '南客隔间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '249'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '301' AND r2.room_unit = '3'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南客隔间'
WHERE b.building_no = '249' AND r.room_no = '301' AND r.room_unit = '3';

-- 249-301-4
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '301', '4', '南带飘窗间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '249'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '301' AND r2.room_unit = '4'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南带飘窗间'
WHERE b.building_no = '249' AND r.room_no = '301' AND r.room_unit = '4';

-- 249-301-5
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '301', '5', '南独卫', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '249'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '301' AND r2.room_unit = '5'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南独卫'
WHERE b.building_no = '249' AND r.room_no = '301' AND r.room_unit = '5';

-- 249-302-1
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '302', '1', '北小单间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '249'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '302' AND r2.room_unit = '1'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '北小单间'
WHERE b.building_no = '249' AND r.room_no = '302' AND r.room_unit = '1';

-- 249-302-2
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '302', '2', '北厨房隔间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '249'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '302' AND r2.room_unit = '2'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '北厨房隔间'
WHERE b.building_no = '249' AND r.room_no = '302' AND r.room_unit = '2';

-- 249-302-3
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '302', '3', '南带飘窗间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '249'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '302' AND r2.room_unit = '3'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南带飘窗间'
WHERE b.building_no = '249' AND r.room_no = '302' AND r.room_unit = '3';

-- 249-302-4
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '302', '4', '南独卫', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '249'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '302' AND r2.room_unit = '4'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南独卫'
WHERE b.building_no = '249' AND r.room_no = '302' AND r.room_unit = '4';

-- 249-302-5
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '302', '5', '南客隔间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '249'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '302' AND r2.room_unit = '5'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南客隔间'
WHERE b.building_no = '249' AND r.room_no = '302' AND r.room_unit = '5';

-- 249-401-1
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '401', '1', '北小单间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '249'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '401' AND r2.room_unit = '1'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '北小单间'
WHERE b.building_no = '249' AND r.room_no = '401' AND r.room_unit = '1';

-- 249-401-2
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '401', '2', '北厨房隔间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '249'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '401' AND r2.room_unit = '2'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '北厨房隔间'
WHERE b.building_no = '249' AND r.room_no = '401' AND r.room_unit = '2';

-- 249-401-3
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '401', '3', '南客隔间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '249'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '401' AND r2.room_unit = '3'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南客隔间'
WHERE b.building_no = '249' AND r.room_no = '401' AND r.room_unit = '3';

-- 249-401-4
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '401', '4', '南带飘窗间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '249'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '401' AND r2.room_unit = '4'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南带飘窗间'
WHERE b.building_no = '249' AND r.room_no = '401' AND r.room_unit = '4';

-- 249-401-5
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '401', '5', '南独卫', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '249'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '401' AND r2.room_unit = '5'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南独卫'
WHERE b.building_no = '249' AND r.room_no = '401' AND r.room_unit = '5';

-- 249-402-1
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '402', '1', '北小单间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '249'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '402' AND r2.room_unit = '1'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '北小单间'
WHERE b.building_no = '249' AND r.room_no = '402' AND r.room_unit = '1';

-- 249-402-2
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '402', '2', '北厨房隔间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '249'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '402' AND r2.room_unit = '2'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '北厨房隔间'
WHERE b.building_no = '249' AND r.room_no = '402' AND r.room_unit = '2';

-- 249-402-3
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '402', '3', '南客隔间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '249'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '402' AND r2.room_unit = '3'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南客隔间'
WHERE b.building_no = '249' AND r.room_no = '402' AND r.room_unit = '3';

-- 249-402-4
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '402', '4', '南带飘窗间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '249'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '402' AND r2.room_unit = '4'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南带飘窗间'
WHERE b.building_no = '249' AND r.room_no = '402' AND r.room_unit = '4';

-- 249-402-5
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '402', '5', '南独卫', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '249'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '402' AND r2.room_unit = '5'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南独卫'
WHERE b.building_no = '249' AND r.room_no = '402' AND r.room_unit = '5';

-- 250-202-1
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '202', '1', '客改间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '250'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '202' AND r2.room_unit = '1'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '客改间'
WHERE b.building_no = '250' AND r.room_no = '202' AND r.room_unit = '1';

-- 250-202-2
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '202', '2', '南飘窗', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '250'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '202' AND r2.room_unit = '2'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南飘窗'
WHERE b.building_no = '250' AND r.room_no = '202' AND r.room_unit = '2';

-- 250-202-3
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '202', '3', '独立卫生间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '250'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '202' AND r2.room_unit = '3'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '独立卫生间'
WHERE b.building_no = '250' AND r.room_no = '202' AND r.room_unit = '3';

-- 250-202-4
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '202', '4', '北小单间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '250'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '202' AND r2.room_unit = '4'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '北小单间'
WHERE b.building_no = '250' AND r.room_no = '202' AND r.room_unit = '4';

-- 250-202-5
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '202', '5', '北厨改', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '250'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '202' AND r2.room_unit = '5'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '北厨改'
WHERE b.building_no = '250' AND r.room_no = '202' AND r.room_unit = '5';

-- 250-202-6
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '202', '6', '北厨改套间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '250'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '202' AND r2.room_unit = '6'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '北厨改套间'
WHERE b.building_no = '250' AND r.room_no = '202' AND r.room_unit = '6';

-- 250-301-1
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '301', '1', '北小单间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '250'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '301' AND r2.room_unit = '1'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '北小单间'
WHERE b.building_no = '250' AND r.room_no = '301' AND r.room_unit = '1';

-- 250-301-2
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '301', '2', '北厨房隔间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '250'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '301' AND r2.room_unit = '2'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '北厨房隔间'
WHERE b.building_no = '250' AND r.room_no = '301' AND r.room_unit = '2';

-- 250-301-3
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '301', '3', '南客隔间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '250'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '301' AND r2.room_unit = '3'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南客隔间'
WHERE b.building_no = '250' AND r.room_no = '301' AND r.room_unit = '3';

-- 250-301-4
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '301', '4', '南带飘窗间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '250'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '301' AND r2.room_unit = '4'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南带飘窗间'
WHERE b.building_no = '250' AND r.room_no = '301' AND r.room_unit = '4';

-- 250-301-5
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '301', '5', '南独卫', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '250'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '301' AND r2.room_unit = '5'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南独卫'
WHERE b.building_no = '250' AND r.room_no = '301' AND r.room_unit = '5';

-- 250-302-1
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '302', '1', '客改间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '250'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '302' AND r2.room_unit = '1'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '客改间'
WHERE b.building_no = '250' AND r.room_no = '302' AND r.room_unit = '1';

-- 250-302-2
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '302', '2', '南飘窗', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '250'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '302' AND r2.room_unit = '2'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南飘窗'
WHERE b.building_no = '250' AND r.room_no = '302' AND r.room_unit = '2';

-- 250-302-3
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '302', '3', '独立卫生间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '250'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '302' AND r2.room_unit = '3'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '独立卫生间'
WHERE b.building_no = '250' AND r.room_no = '302' AND r.room_unit = '3';

-- 250-302-4
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '302', '4', '北小单间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '250'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '302' AND r2.room_unit = '4'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '北小单间'
WHERE b.building_no = '250' AND r.room_no = '302' AND r.room_unit = '4';

-- 250-302-5
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '302', '5', '北厨改', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '250'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '302' AND r2.room_unit = '5'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '北厨改'
WHERE b.building_no = '250' AND r.room_no = '302' AND r.room_unit = '5';

-- 250-302-6
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '302', '6', '北厨改套间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '250'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '302' AND r2.room_unit = '6'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '北厨改套间'
WHERE b.building_no = '250' AND r.room_no = '302' AND r.room_unit = '6';

-- 250-401（女生宿舍）-1
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '401（女生宿舍）', '1', '北小单间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '250'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '401（女生宿舍）' AND r2.room_unit = '1'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '北小单间'
WHERE b.building_no = '250' AND r.room_no = '401（女生宿舍）' AND r.room_unit = '1';

-- 250-401（女生宿舍）-2
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '401（女生宿舍）', '2', '北厨房隔间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '250'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '401（女生宿舍）' AND r2.room_unit = '2'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '北厨房隔间'
WHERE b.building_no = '250' AND r.room_no = '401（女生宿舍）' AND r.room_unit = '2';

-- 250-401（女生宿舍）-3
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '401（女生宿舍）', '3', '南客隔间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '250'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '401（女生宿舍）' AND r2.room_unit = '3'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南客隔间'
WHERE b.building_no = '250' AND r.room_no = '401（女生宿舍）' AND r.room_unit = '3';

-- 250-401（女生宿舍）-4
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '401（女生宿舍）', '4', '南带飘窗间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '250'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '401（女生宿舍）' AND r2.room_unit = '4'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南带飘窗间'
WHERE b.building_no = '250' AND r.room_no = '401（女生宿舍）' AND r.room_unit = '4';

-- 250-401（女生宿舍）-5
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '401（女生宿舍）', '5', '南独卫', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '250'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '401（女生宿舍）' AND r2.room_unit = '5'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南独卫'
WHERE b.building_no = '250' AND r.room_no = '401（女生宿舍）' AND r.room_unit = '5';

-- 250-402（女生宿舍）-1
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '402（女生宿舍）', '1', '北小单间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '250'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '402（女生宿舍）' AND r2.room_unit = '1'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '北小单间'
WHERE b.building_no = '250' AND r.room_no = '402（女生宿舍）' AND r.room_unit = '1';

-- 250-402（女生宿舍）-2
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '402（女生宿舍）', '2', '北厨房隔间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '250'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '402（女生宿舍）' AND r2.room_unit = '2'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '北厨房隔间'
WHERE b.building_no = '250' AND r.room_no = '402（女生宿舍）' AND r.room_unit = '2';

-- 250-402（女生宿舍）-3
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '402（女生宿舍）', '3', '南客隔间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '250'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '402（女生宿舍）' AND r2.room_unit = '3'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南客隔间'
WHERE b.building_no = '250' AND r.room_no = '402（女生宿舍）' AND r.room_unit = '3';

-- 250-402（女生宿舍）-4
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '402（女生宿舍）', '4', '南带飘窗间', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '250'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '402（女生宿舍）' AND r2.room_unit = '4'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南带飘窗间'
WHERE b.building_no = '250' AND r.room_no = '402（女生宿舍）' AND r.room_unit = '4';

-- 250-402（女生宿舍）-5
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '402（女生宿舍）', '5', '南独卫', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '250'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '402（女生宿舍）' AND r2.room_unit = '5'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南独卫'
WHERE b.building_no = '250' AND r.room_no = '402（女生宿舍）' AND r.room_unit = '5';

-- 99-45-402（女生宿舍）-1
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '402（女生宿舍）', '1', '客改南卧室', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '99-45'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '402（女生宿舍）' AND r2.room_unit = '1'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '客改南卧室'
WHERE b.building_no = '99-45' AND r.room_no = '402（女生宿舍）' AND r.room_unit = '1';

-- 99-45-402（女生宿舍）-2
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '402（女生宿舍）', '2', '车库北卧室', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '99-45'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '402（女生宿舍）' AND r2.room_unit = '2'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '车库北卧室'
WHERE b.building_no = '99-45' AND r.room_no = '402（女生宿舍）' AND r.room_unit = '2';

-- 99-45-402（女生宿舍）-3
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '402（女生宿舍）', '3', '南大阳台', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '99-45'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '402（女生宿舍）' AND r2.room_unit = '3'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南大阳台'
WHERE b.building_no = '99-45' AND r.room_no = '402（女生宿舍）' AND r.room_unit = '3';

-- 99-45-402（女生宿舍）-4
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '402（女生宿舍）', '4', '北小阳台', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '99-45'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '402（女生宿舍）' AND r2.room_unit = '4'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '北小阳台'
WHERE b.building_no = '99-45' AND r.room_no = '402（女生宿舍）' AND r.room_unit = '4';

-- 99-45-402（女生宿舍）-5
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '402（女生宿舍）', '5', '无阳台', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '99-45'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '402（女生宿舍）' AND r2.room_unit = '5'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '无阳台'
WHERE b.building_no = '99-45' AND r.room_no = '402（女生宿舍）' AND r.room_unit = '5';

-- 99-46-402（女生宿舍）-1
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '402（女生宿舍）', '1', '车库北卧室', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '99-46'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '402（女生宿舍）' AND r2.room_unit = '1'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '车库北卧室'
WHERE b.building_no = '99-46' AND r.room_no = '402（女生宿舍）' AND r.room_unit = '1';

-- 99-46-402（女生宿舍）-2
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '402（女生宿舍）', '2', '客改南卧室', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '99-46'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '402（女生宿舍）' AND r2.room_unit = '2'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '客改南卧室'
WHERE b.building_no = '99-46' AND r.room_no = '402（女生宿舍）' AND r.room_unit = '2';

-- 99-46-402（女生宿舍）-3
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '402（女生宿舍）', '3', '南大阳台', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '99-46'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '402（女生宿舍）' AND r2.room_unit = '3'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南大阳台'
WHERE b.building_no = '99-46' AND r.room_no = '402（女生宿舍）' AND r.room_unit = '3';

-- 99-46-402（女生宿舍）-4
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '402（女生宿舍）', '4', '北小阳台', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '99-46'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '402（女生宿舍）' AND r2.room_unit = '4'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '北小阳台'
WHERE b.building_no = '99-46' AND r.room_no = '402（女生宿舍）' AND r.room_unit = '4';

-- 99-46-402（女生宿舍）-5
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '402（女生宿舍）', '5', '无阳台', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '99-46'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '402（女生宿舍）' AND r2.room_unit = '5'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '无阳台'
WHERE b.building_no = '99-46' AND r.room_no = '402（女生宿舍）' AND r.room_unit = '5';

-- 99-83-402（女生宿舍）-1
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '402（女生宿舍）', '1', '二楼北小阳台', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '99-83'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '402（女生宿舍）' AND r2.room_unit = '1'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '二楼北小阳台'
WHERE b.building_no = '99-83' AND r.room_no = '402（女生宿舍）' AND r.room_unit = '1';

-- 99-83-402（女生宿舍）-2
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '402（女生宿舍）', '2', '二楼南大阳台', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '99-83'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '402（女生宿舍）' AND r2.room_unit = '2'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '二楼南大阳台'
WHERE b.building_no = '99-83' AND r.room_no = '402（女生宿舍）' AND r.room_unit = '2';

-- 99-83-402（女生宿舍）-3
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '402（女生宿舍）', '3', '二楼无阳台', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '99-83'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '402（女生宿舍）' AND r2.room_unit = '3'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '二楼无阳台'
WHERE b.building_no = '99-83' AND r.room_no = '402（女生宿舍）' AND r.room_unit = '3';

-- 99-83-402（女生宿舍）-4
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '402（女生宿舍）', '4', '一楼车库北卧室', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '99-83'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '402（女生宿舍）' AND r2.room_unit = '4'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '一楼车库北卧室'
WHERE b.building_no = '99-83' AND r.room_no = '402（女生宿舍）' AND r.room_unit = '4';

-- 99-83-402（女生宿舍）-5
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '402（女生宿舍）', '5', '一楼南卧室', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '99-83'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '402（女生宿舍）' AND r2.room_unit = '5'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '一楼南卧室'
WHERE b.building_no = '99-83' AND r.room_no = '402（女生宿舍）' AND r.room_unit = '5';

-- 99-84-402（女生宿舍）-1
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '402（女生宿舍）', '1', '客改南卧室', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '99-84'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '402（女生宿舍）' AND r2.room_unit = '1'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '客改南卧室'
WHERE b.building_no = '99-84' AND r.room_no = '402（女生宿舍）' AND r.room_unit = '1';

-- 99-84-402（女生宿舍）-2
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '402（女生宿舍）', '2', '车库北卧室', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '99-84'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '402（女生宿舍）' AND r2.room_unit = '2'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '车库北卧室'
WHERE b.building_no = '99-84' AND r.room_no = '402（女生宿舍）' AND r.room_unit = '2';

-- 99-84-402（女生宿舍）-3
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '402（女生宿舍）', '3', '南大阳台', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '99-84'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '402（女生宿舍）' AND r2.room_unit = '3'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '南大阳台'
WHERE b.building_no = '99-84' AND r.room_no = '402（女生宿舍）' AND r.room_unit = '3';

-- 99-84-402（女生宿舍）-4
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '402（女生宿舍）', '4', '北小阳台', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '99-84'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '402（女生宿舍）' AND r2.room_unit = '4'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '北小阳台'
WHERE b.building_no = '99-84' AND r.room_no = '402（女生宿舍）' AND r.room_unit = '4';

-- 99-84-402（女生宿舍）-5
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '402（女生宿舍）', '5', '无阳台', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '99-84'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '402（女生宿舍）' AND r2.room_unit = '5'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '无阳台'
WHERE b.building_no = '99-84' AND r.room_no = '402（女生宿舍）' AND r.room_unit = '5';

