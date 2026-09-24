-- 为房间表的状态字段添加 'idle' 选项
-- 注意：MySQL 不支持直接修改 ENUM，需要先删除再重新创建

-- 1. 先修改表，将 status 改为 VARCHAR（临时）
ALTER TABLE rooms MODIFY COLUMN status VARCHAR(20) NOT NULL DEFAULT 'active';

-- 2. 删除旧的 ENUM 类型
-- MySQL 会自动处理

-- 3. 重新创建 ENUM 类型（包含新的 idle 状态）
ALTER TABLE rooms MODIFY COLUMN status ENUM('active', 'inactive', 'idle') NOT NULL DEFAULT 'active';

-- 4. 可选：将符合条件的房间设置为空闲状态
-- UPDATE rooms SET status = 'idle' WHERE ... (根据业务需求设置)
