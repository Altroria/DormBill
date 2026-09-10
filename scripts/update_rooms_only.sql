-- 房间数据更新SQL（仅更新已存在的房间）

-- 设置字符集
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '1', r.room_name = '北小单间'
WHERE b.building_no = '247' AND r.room_no = '201';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '2', r.room_name = '南隔间'
WHERE b.building_no = '247' AND r.room_no = '201';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '3', r.room_name = '南带飘窗间'
WHERE b.building_no = '247' AND r.room_no = '201';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '4', r.room_name = '南独卫'
WHERE b.building_no = '247' AND r.room_no = '201';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '1', r.room_name = '南独卫'
WHERE b.building_no = '247' AND r.room_no = '202';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '2', r.room_name = '北小单间'
WHERE b.building_no = '247' AND r.room_no = '202';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '3', r.room_name = '南隔间'
WHERE b.building_no = '247' AND r.room_no = '202';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '4', r.room_name = '南带飘窗间'
WHERE b.building_no = '247' AND r.room_no = '202';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '1', r.room_name = '北厨房隔间'
WHERE b.building_no = '248' AND r.room_no = '301';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '2', r.room_name = '北小单间'
WHERE b.building_no = '248' AND r.room_no = '301';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '3', r.room_name = '南客隔间'
WHERE b.building_no = '248' AND r.room_no = '301';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '4', r.room_name = '南带飘窗间'
WHERE b.building_no = '248' AND r.room_no = '301';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '5', r.room_name = '南独卫'
WHERE b.building_no = '248' AND r.room_no = '301';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '1', r.room_name = '北厨房隔间'
WHERE b.building_no = '248' AND r.room_no = '302';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '2', r.room_name = '北小单间'
WHERE b.building_no = '248' AND r.room_no = '302';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '3', r.room_name = '南客隔间'
WHERE b.building_no = '248' AND r.room_no = '302';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '4', r.room_name = '南带飘窗间'
WHERE b.building_no = '248' AND r.room_no = '302';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '5', r.room_name = '南独卫'
WHERE b.building_no = '248' AND r.room_no = '302';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '1', r.room_name = '客改间'
WHERE b.building_no = '248' AND r.room_no = '401';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '2', r.room_name = '南飘窗'
WHERE b.building_no = '248' AND r.room_no = '401';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '3', r.room_name = '独立卫生间'
WHERE b.building_no = '248' AND r.room_no = '401';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '4', r.room_name = '北小单间'
WHERE b.building_no = '248' AND r.room_no = '401';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '5', r.room_name = '北厨改'
WHERE b.building_no = '248' AND r.room_no = '401';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '6', r.room_name = '北厨改套间'
WHERE b.building_no = '248' AND r.room_no = '401';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '1', r.room_name = '北厨房隔间'
WHERE b.building_no = '248' AND r.room_no = '402';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '2', r.room_name = '北小单间'
WHERE b.building_no = '248' AND r.room_no = '402';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '3', r.room_name = '南客隔间'
WHERE b.building_no = '248' AND r.room_no = '402';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '4', r.room_name = '南带飘窗间'
WHERE b.building_no = '248' AND r.room_no = '402';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '5', r.room_name = '南独卫'
WHERE b.building_no = '248' AND r.room_no = '402';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '1', r.room_name = '北厨房隔间'
WHERE b.building_no = '249' AND r.room_no = '201';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '2', r.room_name = ''
WHERE b.building_no = '249' AND r.room_no = '201';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '3', r.room_name = '南独卫'
WHERE b.building_no = '249' AND r.room_no = '201';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '1', r.room_name = '北小单间'
WHERE b.building_no = '249' AND r.room_no = '301';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '2', r.room_name = '北厨房隔间'
WHERE b.building_no = '249' AND r.room_no = '301';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '3', r.room_name = '南客隔间'
WHERE b.building_no = '249' AND r.room_no = '301';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '4', r.room_name = '南带飘窗间'
WHERE b.building_no = '249' AND r.room_no = '301';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '5', r.room_name = '南独卫'
WHERE b.building_no = '249' AND r.room_no = '301';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '1', r.room_name = '北小单间'
WHERE b.building_no = '249' AND r.room_no = '302';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '2', r.room_name = '北厨房隔间'
WHERE b.building_no = '249' AND r.room_no = '302';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '3', r.room_name = '南带飘窗间'
WHERE b.building_no = '249' AND r.room_no = '302';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '4', r.room_name = '南独卫'
WHERE b.building_no = '249' AND r.room_no = '302';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '5', r.room_name = '南客隔间'
WHERE b.building_no = '249' AND r.room_no = '302';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '1', r.room_name = '北小单间'
WHERE b.building_no = '249' AND r.room_no = '401';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '2', r.room_name = '北厨房隔间'
WHERE b.building_no = '249' AND r.room_no = '401';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '3', r.room_name = '南客隔间'
WHERE b.building_no = '249' AND r.room_no = '401';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '4', r.room_name = '南带飘窗间'
WHERE b.building_no = '249' AND r.room_no = '401';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '5', r.room_name = '南独卫'
WHERE b.building_no = '249' AND r.room_no = '401';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '1', r.room_name = '北小单间'
WHERE b.building_no = '249' AND r.room_no = '402';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '2', r.room_name = '北厨房隔间'
WHERE b.building_no = '249' AND r.room_no = '402';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '3', r.room_name = '南客隔间'
WHERE b.building_no = '249' AND r.room_no = '402';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '4', r.room_name = '南带飘窗间'
WHERE b.building_no = '249' AND r.room_no = '402';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '5', r.room_name = '南独卫'
WHERE b.building_no = '249' AND r.room_no = '402';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '1', r.room_name = '客改间'
WHERE b.building_no = '250' AND r.room_no = '202';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '2', r.room_name = '南飘窗'
WHERE b.building_no = '250' AND r.room_no = '202';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '3', r.room_name = '独立卫生间'
WHERE b.building_no = '250' AND r.room_no = '202';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '4', r.room_name = '北小单间'
WHERE b.building_no = '250' AND r.room_no = '202';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '5', r.room_name = '北厨改'
WHERE b.building_no = '250' AND r.room_no = '202';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '6', r.room_name = '北厨改套间'
WHERE b.building_no = '250' AND r.room_no = '202';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '1', r.room_name = '北小单间'
WHERE b.building_no = '250' AND r.room_no = '301';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '2', r.room_name = '北厨房隔间'
WHERE b.building_no = '250' AND r.room_no = '301';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '3', r.room_name = '南客隔间'
WHERE b.building_no = '250' AND r.room_no = '301';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '4', r.room_name = '南带飘窗间'
WHERE b.building_no = '250' AND r.room_no = '301';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '5', r.room_name = '南独卫'
WHERE b.building_no = '250' AND r.room_no = '301';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '1', r.room_name = '客改间'
WHERE b.building_no = '250' AND r.room_no = '302';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '2', r.room_name = '南飘窗'
WHERE b.building_no = '250' AND r.room_no = '302';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '3', r.room_name = '独立卫生间'
WHERE b.building_no = '250' AND r.room_no = '302';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '4', r.room_name = '北小单间'
WHERE b.building_no = '250' AND r.room_no = '302';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '5', r.room_name = '北厨改'
WHERE b.building_no = '250' AND r.room_no = '302';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '6', r.room_name = '北厨改套间'
WHERE b.building_no = '250' AND r.room_no = '302';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '1', r.room_name = '北小单间'
WHERE b.building_no = '250' AND r.room_no = '401（女生宿舍）';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '2', r.room_name = '北厨房隔间'
WHERE b.building_no = '250' AND r.room_no = '401（女生宿舍）';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '3', r.room_name = '南客隔间'
WHERE b.building_no = '250' AND r.room_no = '401（女生宿舍）';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '4', r.room_name = '南带飘窗间'
WHERE b.building_no = '250' AND r.room_no = '401（女生宿舍）';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '5', r.room_name = '南独卫'
WHERE b.building_no = '250' AND r.room_no = '401（女生宿舍）';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '1', r.room_name = '北小单间'
WHERE b.building_no = '250' AND r.room_no = '402（女生宿舍）';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '2', r.room_name = '北厨房隔间'
WHERE b.building_no = '250' AND r.room_no = '402（女生宿舍）';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '3', r.room_name = '南客隔间'
WHERE b.building_no = '250' AND r.room_no = '402（女生宿舍）';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '4', r.room_name = '南带飘窗间'
WHERE b.building_no = '250' AND r.room_no = '402（女生宿舍）';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '5', r.room_name = '南独卫'
WHERE b.building_no = '250' AND r.room_no = '402（女生宿舍）';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '1', r.room_name = '客改南卧室'
WHERE b.building_no = '99-45' AND r.room_no = '402（女生宿舍）';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '2', r.room_name = '车库北卧室'
WHERE b.building_no = '99-45' AND r.room_no = '402（女生宿舍）';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '3', r.room_name = '南大阳台'
WHERE b.building_no = '99-45' AND r.room_no = '402（女生宿舍）';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '4', r.room_name = '北小阳台'
WHERE b.building_no = '99-45' AND r.room_no = '402（女生宿舍）';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '5', r.room_name = '无阳台'
WHERE b.building_no = '99-45' AND r.room_no = '402（女生宿舍）';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '1', r.room_name = '车库北卧室'
WHERE b.building_no = '99-46' AND r.room_no = '402（女生宿舍）';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '2', r.room_name = '客改南卧室'
WHERE b.building_no = '99-46' AND r.room_no = '402（女生宿舍）';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '3', r.room_name = '南大阳台'
WHERE b.building_no = '99-46' AND r.room_no = '402（女生宿舍）';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '4', r.room_name = '北小阳台'
WHERE b.building_no = '99-46' AND r.room_no = '402（女生宿舍）';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '5', r.room_name = '无阳台'
WHERE b.building_no = '99-46' AND r.room_no = '402（女生宿舍）';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '1', r.room_name = '二楼北小阳台'
WHERE b.building_no = '99-83' AND r.room_no = '402（女生宿舍）';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '2', r.room_name = '二楼南大阳台'
WHERE b.building_no = '99-83' AND r.room_no = '402（女生宿舍）';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '3', r.room_name = '二楼无阳台'
WHERE b.building_no = '99-83' AND r.room_no = '402（女生宿舍）';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '4', r.room_name = '一楼车库北卧室'
WHERE b.building_no = '99-83' AND r.room_no = '402（女生宿舍）';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '5', r.room_name = '一楼南卧室'
WHERE b.building_no = '99-83' AND r.room_no = '402（女生宿舍）';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '1', r.room_name = '客改南卧室'
WHERE b.building_no = '99-84' AND r.room_no = '402（女生宿舍）';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '2', r.room_name = '车库北卧室'
WHERE b.building_no = '99-84' AND r.room_no = '402（女生宿舍）';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '3', r.room_name = '南大阳台'
WHERE b.building_no = '99-84' AND r.room_no = '402（女生宿舍）';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '4', r.room_name = '北小阳台'
WHERE b.building_no = '99-84' AND r.room_no = '402（女生宿舍）';

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '5', r.room_name = '无阳台'
WHERE b.building_no = '99-84' AND r.room_no = '402（女生宿舍）';

