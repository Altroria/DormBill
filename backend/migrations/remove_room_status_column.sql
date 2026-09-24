-- 删除 rooms 表的 status 字段（状态现在由入住记录动态计算）
-- 执行前请备份数据库

ALTER TABLE rooms DROP COLUMN status;
