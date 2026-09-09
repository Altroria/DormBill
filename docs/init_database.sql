-- 蓉蓉的收租小工具 - 数据库初始化脚本
-- 创建数据库
CREATE DATABASE IF NOT EXISTS dormbill CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE dormbill;

-- 注意：表结构由 SQLAlchemy ORM 自动创建
-- 运行 backend/run.py 时会自动创建所有表
-- 本脚本仅用于手动数据库初始化（可选）

-- 示例数据（可选）
-- 插入示例楼栋
-- INSERT INTO buildings (building_no, name, status) VALUES ('247', '247栋', 'active');
-- INSERT INTO buildings (building_no, name, status) VALUES ('248', '248栋', 'active');

-- 插入示例员工
-- INSERT INTO employees (employee_no, name, company, department, position, status) 
-- VALUES ('E001', '张三', '天泽', '加工部', '加工部技术员', 'active');
