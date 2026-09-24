-- 添加客房标识字段
ALTER TABLE rooms 
ADD COLUMN is_guest_room TINYINT(1) DEFAULT 0 COMMENT '是否为客房（客房水电租全免）' AFTER rent_standard;

-- 为该字段添加索引（方便快速筛选客房）
CREATE INDEX idx_is_guest_room ON rooms(is_guest_room);
