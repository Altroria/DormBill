-- 7月份数据导入脚本
-- 生成时间: 2026-09-10 15:50:35

USE dormbill;

-- ======================================
-- 1. 插入楼栋数据
-- ======================================
INSERT INTO buildings (building_no, name, status, created_at, updated_at) VALUES ('247', '247栋', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO buildings (building_no, name, status, created_at, updated_at) VALUES ('248', '248栋', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO buildings (building_no, name, status, created_at, updated_at) VALUES ('249', '249栋', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO buildings (building_no, name, status, created_at, updated_at) VALUES ('250', '250栋', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO buildings (building_no, name, status, created_at, updated_at) VALUES ('99-45', '99-45栋', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO buildings (building_no, name, status, created_at, updated_at) VALUES ('99-46', '99-46栋', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO buildings (building_no, name, status, created_at, updated_at) VALUES ('99-83', '99-83栋', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO buildings (building_no, name, status, created_at, updated_at) VALUES ('99-84', '99-84栋', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();

-- ======================================
-- 2. 插入房间数据
-- ======================================
INSERT INTO rooms (building_id, room_no, room_name, status, created_at, updated_at) SELECT b.id, '201', '北小单间', 'active', NOW(), NOW() FROM buildings b WHERE b.building_no = '247' ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO rooms (building_id, room_no, room_name, status, created_at, updated_at) SELECT b.id, '202', '南独卫', 'active', NOW(), NOW() FROM buildings b WHERE b.building_no = '247' ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO rooms (building_id, room_no, room_name, status, created_at, updated_at) SELECT b.id, '301', '北厨房隔间', 'active', NOW(), NOW() FROM buildings b WHERE b.building_no = '248' ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO rooms (building_id, room_no, room_name, status, created_at, updated_at) SELECT b.id, '302', '北厨房隔间', 'active', NOW(), NOW() FROM buildings b WHERE b.building_no = '248' ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO rooms (building_id, room_no, room_name, status, created_at, updated_at) SELECT b.id, '402', '北厨房隔间', 'active', NOW(), NOW() FROM buildings b WHERE b.building_no = '248' ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO rooms (building_id, room_no, room_name, status, created_at, updated_at) SELECT b.id, '201', '北厨房隔间', 'active', NOW(), NOW() FROM buildings b WHERE b.building_no = '249' ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO rooms (building_id, room_no, room_name, status, created_at, updated_at) SELECT b.id, '301', '北小单间', 'active', NOW(), NOW() FROM buildings b WHERE b.building_no = '249' ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO rooms (building_id, room_no, room_name, status, created_at, updated_at) SELECT b.id, '302', '北小单间', 'active', NOW(), NOW() FROM buildings b WHERE b.building_no = '249' ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO rooms (building_id, room_no, room_name, status, created_at, updated_at) SELECT b.id, '401', '北小单间', 'active', NOW(), NOW() FROM buildings b WHERE b.building_no = '249' ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO rooms (building_id, room_no, room_name, status, created_at, updated_at) SELECT b.id, '402', '北小单间', 'active', NOW(), NOW() FROM buildings b WHERE b.building_no = '249' ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO rooms (building_id, room_no, room_name, status, created_at, updated_at) SELECT b.id, '301', '北小单间', 'active', NOW(), NOW() FROM buildings b WHERE b.building_no = '250' ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO rooms (building_id, room_no, room_name, status, created_at, updated_at) SELECT b.id, '302', '南飘窗', 'active', NOW(), NOW() FROM buildings b WHERE b.building_no = '250' ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO rooms (building_id, room_no, room_name, status, remark, created_at, updated_at) SELECT b.id, '401', '北小单间', 'active', '女生宿舍', NOW(), NOW() FROM buildings b WHERE b.building_no = '250' ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO rooms (building_id, room_no, room_name, status, remark, created_at, updated_at) SELECT b.id, '402', '北小单间', 'active', '女生宿舍', NOW(), NOW() FROM buildings b WHERE b.building_no = '250' ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO rooms (building_id, room_no, room_name, status, remark, created_at, updated_at) SELECT b.id, '402', '客改南卧室', 'active', '女生宿舍', NOW(), NOW() FROM buildings b WHERE b.building_no = '99-45' ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO rooms (building_id, room_no, room_name, status, remark, created_at, updated_at) SELECT b.id, '402', '车库北卧室', 'active', '女生宿舍', NOW(), NOW() FROM buildings b WHERE b.building_no = '99-46' ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO rooms (building_id, room_no, room_name, status, remark, created_at, updated_at) SELECT b.id, '402', '二楼北小阳台', 'active', '女生宿舍', NOW(), NOW() FROM buildings b WHERE b.building_no = '99-83' ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO rooms (building_id, room_no, room_name, status, remark, created_at, updated_at) SELECT b.id, '402', '客改南卧室', 'active', '女生宿舍', NOW(), NOW() FROM buildings b WHERE b.building_no = '99-84' ON DUPLICATE KEY UPDATE updated_at=NOW();

-- ======================================
-- 3. 插入员工数据
-- ======================================
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0001', '乔亚冬', '天泽', '塑模部', '设计学员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0002', '于乐乐', '天泽', '加工部', '加工部学员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0003', '仲生荣', '天泽', '冲压模具部', '冲压模具部报价工程师', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0004', '何海洋', '拓施培', '拓施培', '工程师', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0005', '冯敏', '天泽', '塑模二部', '塑模二部工程师', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0006', '冯晶琳', '天泽', '', '品检学员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0007', '冯金平', '天檀', '注塑部', '注塑部技术员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0008', '刘佳慧', '天泽', '品质管理部', '测量室', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0009', '刘旭', '天泽', '塑模二部', '设计工程师', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0010', '刘磊', '天泽', '品质部', '品质部检验员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0011', '包康', '拓施培', '拓施培', '工程师', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0012', '单振荡', '天泽', '加工部', '加工部铣床技师', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0013', '吕立永(夜班）', '天泽', '加工部', '加工部CNC操机技师', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0014', '周可才', '天泽', '冲压模具部', '冲压模具部技术员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0015', '周红军', '天泽', '冲模部', '组模技师', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0016', '周艳龙', '天泽', '加工部', 'CNC主管', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0017', '唐历', '天泽', '塑模一部', '塑模一部工程师', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0018', '姚新奥', '拓施培', '拓施培', '实习生', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0019', '姚贵川', '天泽', '塑模二部', '塑模二部学员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0020', '孙俊', '天泽', '加工部', '加工部CNC编程学员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0021', '孙彦超', '天檀', '注塑部', '注塑部技术员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0022', '孙晨朔', '拓施培', '拓施培', '工程师', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0023', '孙波', '天泽', '加工部', '学员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0024', '孙洪力', '天泽', '塑模二部', '产品工程', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0025', '孙涛', '天泽', '塑模一部', '塑模一部技术学员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0026', '孙闯营', '天檀', '注塑部', '注塑部主管', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0027', '宋显迪', '天泽', '塑模一部', '塑模一部技术员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0028', '宫凤云', '天泽', '加工部', '加工部铣床组长', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0029', '尚歆舒', '天泽', '', '', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0030', '尹杰', '天泽', '加工部', '加工部CNC操机技师', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0031', '庄荣飞', '拓施培', '拓施培', '工程师', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0032', '张志胜', '天泽', '模具事业部', '生管计划', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0033', '张月东', '天泽', '加工部', 'CHC编程技师', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0034', '张甲坤', '天檀', '品质部', '工程师', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0035', '张聪', '天檀', '品质部', '品质部经理', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0036', '张英华', '天泽', '加工部', '加工部CNC操机技师', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0037', '张鹏超', '天泽', '加工部', 'CNC编程技师', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0038', '方奇锋', '天泽', '加工部', '加工部慢走丝技师', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0039', '方子健', '天泽', '塑模二部', '钳工学员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0040', '朱国甫', '天泽', '塑模一部', '塑模一部技术员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0041', '朱宇豪', '天泽', '冲压模具部', '冲压模具部学员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0042', '朱时雨', '天泽', '冲压模具部', '冲压模具部技术员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0043', '朱竹青', '天泽', '塑模一部', '塑模一部工程师', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0044', '李东胜', '天泽', '行政部', '厨师', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0045', '李中铭', '天泽', '塑模二部', '塑模二部技术员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0046', '李克宝', '天泽', '塑模一部', '塑模一部技术学员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0047', '李兴海', '天泽', '加工部', '加工部学员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0048', '李加明', '天泽', '加工部', '加工部研磨技师', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0049', '李华丹', '天泽', '塑模二部', '组装技术员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0050', '李家伟', '天檀', '产品工程部', '产品工程师学员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0051', '李成鹏', '天泽', '加工部', '加工部实习生', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0052', '李致远', '拓施培', '拓施培', '实习生', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0053', '李运运', '芜湖', '加工部', '放电部学员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0054', '杨俊杰', '天檀', '产品工程部', '产品工程师学员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0055', '杨城', '拓施培', '工程二部', '机械工程学员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0056', '杨宇', '天泽', '塑模一部', '塑模一部技术员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0057', '林三添', '天檀', '注塑部', '注塑部技术员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0058', '林权', '天泽', '加工部', 'CNC现编程技师', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0059', '梁凤', '天泽', '业务发展', '业务发展项目工程师', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0060', '欧永波', '天泽', '塑模二部', '塑模二部技术员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0061', '殷陈陈', '天泽', '加工部', '加工部CNC操机技师', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0062', '毛志令', '芜湖', '产品工程', '高级经理', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0063', '江歙凤', '天泽', '芜湖', '芜湖项目', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0064', '汪文杰', '天泽', '塑模一部', '塑模一部工程师', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0065', '汪永进', '天泽', '塑模一部', '塑模一部技术员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0066', '洛绒生龙', '天泽', '行政部', '行政人员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0067', '洪学琴', '天泽', '质量部', '质量部检验', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0068', '潘珏', '天檀', '财务部', '财务', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0069', '熊正娣', '天泽', '加工部', '加工部慢走丝技师', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0070', '熊青伟', '天泽', '加工部', '加工部铣床组长', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0071', '王德凯', '天泽', '冲压模具部', '冲压模具部经理', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0072', '王浩然', '天泽', '加工部', '慢丝加工部', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0073', '王鑫', '天泽', '加工部', '电加工', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0074', '秦孝红', '拓施培', '拓施培', '工程师', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0075', '程龙浩', '天泽', '塑模一部', '塑模一部技术学员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0076', '童朝海', '天泽', '加工部', '加工部铣床技师', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0077', '罗国庆', '天泽', '项目部', '项目经理', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0078', '罗雄', '天檀', '品质部', '工程师', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0079', '羊蔚琛', '天泽', '销售', '销售', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0080', '翟飞龙', '天泽', '天泽', '塑模二部', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0081', '肖仁华', '天泽', '塑模一部', '塑模一部工程师', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0082', '胡磊磊', '天泽', '组装部', '组装制造工程师', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0083', '范成杰', '天泽', '冲压模具部', '学员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0084', '范椿泉', '天泽', '塑模二部', '塑模二部技术员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0085', '茹金才', '天泽', '加工部', '加工部采购工程师', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0086', '莫红震', '天泽', '产品工程部', '工程师', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0087', '董邦超', '天泽', '塑模一部', '塑模一部学员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0088', '蔡第强', '天泽', '品质部', '测量员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0089', '薛健华', '拓施培', '拓施培', '工程师', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0090', '袁世梁', '天泽', '行政部', '厨师', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0091', '谢之兴', '天泽', '加工部', '加工部放电技师', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0092', '赵俊毫', '天檀', '冲压部', '冲压部技术员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0093', '赵蒙凯', '芜湖', '模具备件外协', '主管', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0094', '邓亭', '天泽', '冲压模具部', '冲压模具部技术员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0095', '邓涛', '天泽', '加工部', '加工部放电技师', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0096', '邹建', '天泽', '塑模一部', '塑模一部高级经理', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0097', '郭红阳', '天泽', '工程研发', '研发实习生', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0098', '郭雅格', '天泽', '模具部', '设计', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0099', '钱瑞蕾', '天檀', '物流部', '物流部仓管员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0100', '钱纪', '天泽', '塑模一部', '塑模一部学员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0101', '闵晓康', '天泽', '冲压', '临时工', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0102', '陈少华', '天泽', '塑模二部', '组装技术员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0103', '陈强', '天泽', '加工部', '放电学员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0104', '陈清水', '天泽', '加工部', '加工部CNC编程技师', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0105', '陈渝', '天泽', '塑模一部', '塑模一部学员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0106', '陈碧峰', '天泽', '加工部', '加工部慢走丝技师', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0107', '陈顺新', '天泽', '加工部', '加工部放电学员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0108', '陶冲', '天檀', '产品工程部', '产品工程师', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0109', '雷寿燕', '天泽', '行政部', '保洁', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0110', '雷志飞', '天泽', '塑模二部', '产品工程', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0111', '颜红良', '天泽', '塑模一部', '组装技术员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0112', '马翔翔', '天檀', '产品工程部', '产品工程部', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0113', '黄志雄', '天泽', '塑模一部', '塑模一部工程师', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0114', '黄明', '拓施培', '工程二部', '经理', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) VALUES ('E0115', '黄浩然', '天泽', '模具部', '冲模组试学员', 'active', NOW(), NOW()) ON DUPLICATE KEY UPDATE updated_at=NOW();
