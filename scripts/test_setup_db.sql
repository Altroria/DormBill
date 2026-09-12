-- ============================================================
-- 测试库初始化(模拟"运行过所有 alembic 迁移"的状态)
-- 建表 + 补齐 room_unit 列 + 改 room_no 长度为 50
-- ============================================================

DROP DATABASE IF EXISTS dormbill_test;
CREATE DATABASE dormbill_test CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE dormbill_test;

-- 1) buildings
CREATE TABLE buildings (
  id BIGINT NOT NULL AUTO_INCREMENT,
  building_no VARCHAR(20) NOT NULL,
  name VARCHAR(50) DEFAULT NULL,
  address VARCHAR(200) DEFAULT NULL,
  status ENUM('active','inactive') DEFAULT NULL,
  remark VARCHAR(500) DEFAULT NULL,
  created_at DATETIME DEFAULT (now()),
  updated_at DATETIME DEFAULT (now()),
  deleted_at DATETIME DEFAULT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY building_no (building_no),
  KEY idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2) rooms (room_no varchar(50) + room_unit)
CREATE TABLE rooms (
  id BIGINT NOT NULL AUTO_INCREMENT,
  building_id BIGINT NOT NULL,
  room_no VARCHAR(50) NOT NULL,
  room_unit VARCHAR(20) DEFAULT NULL,
  room_name VARCHAR(50) NOT NULL,
  meter_no VARCHAR(50) DEFAULT NULL,
  ac_meter_no VARCHAR(50) DEFAULT NULL,
  electricity_price DECIMAL(10,4) DEFAULT NULL,
  rent_standard DECIMAL(10,2) DEFAULT NULL,
  status ENUM('active','inactive') DEFAULT NULL,
  remark VARCHAR(500) DEFAULT NULL,
  created_at DATETIME DEFAULT (now()),
  updated_at DATETIME DEFAULT (now()),
  deleted_at DATETIME DEFAULT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uk_building_room_name (building_id, room_no, room_name),
  KEY idx_building_room (building_id, room_no),
  CONSTRAINT rooms_ibfk_1 FOREIGN KEY (building_id) REFERENCES buildings(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3) employees
CREATE TABLE employees (
  id BIGINT NOT NULL AUTO_INCREMENT,
  employee_no VARCHAR(30) NOT NULL,
  name VARCHAR(50) NOT NULL,
  company VARCHAR(50) DEFAULT NULL,
  department VARCHAR(50) DEFAULT NULL,
  position VARCHAR(50) DEFAULT NULL,
  status ENUM('active','inactive') DEFAULT NULL,
  remark VARCHAR(500) DEFAULT NULL,
  created_at DATETIME DEFAULT (now()),
  updated_at DATETIME DEFAULT (now()),
  deleted_at DATETIME DEFAULT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY employee_no (employee_no),
  KEY idx_name (name),
  KEY idx_company_dept (company, department)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4) residence_records
CREATE TABLE residence_records (
  id BIGINT NOT NULL AUTO_INCREMENT,
  employee_id BIGINT NOT NULL,
  room_id BIGINT NOT NULL,
  check_in_date DATE NOT NULL,
  check_out_date DATE DEFAULT NULL,
  is_primary_payer INT DEFAULT NULL,
  probation_months INT DEFAULT NULL,
  status ENUM('valid','invalid','business_trip','leave') DEFAULT NULL,
  remark VARCHAR(500) DEFAULT NULL,
  created_at DATETIME DEFAULT (now()),
  updated_at DATETIME DEFAULT (now()),
  PRIMARY KEY (id),
  KEY idx_employee (employee_id),
  KEY idx_room (room_id),
  KEY idx_check_in (check_in_date),
  KEY idx_status (status),
  CONSTRAINT rr_emp FOREIGN KEY (employee_id) REFERENCES employees(id),
  CONSTRAINT rr_room FOREIGN KEY (room_id) REFERENCES rooms(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
