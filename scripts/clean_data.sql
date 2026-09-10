-- 完整重新导入脚本
-- 删除所有现有数据并重新导入

-- 设置字符集
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- 禁用外键检查
SET FOREIGN_KEY_CHECKS = 0;

-- 清空相关表
TRUNCATE TABLE residence_records;
TRUNCATE TABLE rooms;

-- 启用外键检查
SET FOREIGN_KEY_CHECKS = 1;

-- 确认清空成功
SELECT 'Tables truncated successfully' as status;
