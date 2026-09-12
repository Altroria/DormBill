-- =============================================
-- 蓉蓉的收租小工具 - 数据库初始化脚本
-- =============================================
-- 说明：本脚本用于创建 dormbill 数据库
-- 使用方法：
--   1. 以 root 用户登录 MySQL
--   2. 执行此脚本：mysql -u root -p < create_database.sql
-- =============================================

-- 删除已存在的数据库（谨慎使用！）
-- DROP DATABASE IF EXISTS dormbill;

-- 创建数据库
CREATE DATABASE IF NOT EXISTS dormbill
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

-- 显示创建结果
SHOW DATABASES LIKE 'dormbill';

-- 切换到新数据库
USE dormbill;

-- 显示数据库信息
SELECT 
    SCHEMA_NAME as '数据库名',
    DEFAULT_CHARACTER_SET_NAME as '字符集',
    DEFAULT_COLLATION_NAME as '排序规则'
FROM information_schema.SCHEMATA
WHERE SCHEMA_NAME = 'dormbill';

-- =============================================
-- 可选：创建专用数据库用户（生产环境推荐）
-- =============================================
-- 创建用户并授权（根据需要取消注释）
-- CREATE USER IF NOT EXISTS 'dormbill_user'@'localhost' IDENTIFIED BY 'your_password_here';
-- GRANT ALL PRIVILEGES ON dormbill.* TO 'dormbill_user'@'localhost';
-- 
-- -- 允许远程访问（仅开发环境）
-- CREATE USER IF NOT EXISTS 'dormbill_user'@'%' IDENTIFIED BY 'your_password_here';
-- GRANT ALL PRIVILEGES ON dormbill.* TO 'dormbill_user'@'%';
-- 
-- FLUSH PRIVILEGES;
-- 
-- -- 显示授权结果
-- SHOW GRANTS FOR 'dormbill_user'@'localhost';

-- =============================================
-- 数据库创建完成
-- =============================================
SELECT '✅ 数据库 dormbill 创建成功！' as '状态';
