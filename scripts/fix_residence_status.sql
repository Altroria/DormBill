-- 修复入住记录中 status 为 NULL 的数据
-- 运行日期: 2026-09-11

USE dormbill;

-- 1. 查看有多少记录的 status 是 NULL
SELECT COUNT(*) as null_status_count FROM residence_records WHERE status IS NULL;

-- 2. 更新所有 NULL 的 status 为 'valid'（默认有效状态）
UPDATE residence_records 
SET status = 'valid' 
WHERE status IS NULL;

-- 3. 验证更新结果
SELECT COUNT(*) as null_status_count_after FROM residence_records WHERE status IS NULL;

-- 4. 查看更新后的 status 分布
SELECT status, COUNT(*) as count 
FROM residence_records 
GROUP BY status;
