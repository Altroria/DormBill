#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
解析房间和人员数据.xlsx，生成数据库导入SQL
生成：楼栋管理、房间管理、入住管理、员工管理
"""
import pandas as pd
from pathlib import Path
from datetime import datetime
import sys

# 设置输出编码
sys.stdout.reconfigure(encoding='utf-8')

def clean_value(value):
    """清理值，转换为SQL安全格式"""
    if pd.isna(value):
        return 'NULL'
    if isinstance(value, (int, float)):
        return str(int(value))
    # 转义单引号
    return f"'{str(value).replace(chr(39), chr(39)+chr(39))}'"

def generate_buildings_sql(df):
    """生成楼栋表SQL - 匹配 buildings 表结构"""
    buildings = df['楼号'].dropna().unique()
    
    sql = """-- =============================================
-- 楼栋管理数据导入
-- =============================================
INSERT INTO buildings (building_no, name, address, status, remark, created_at, updated_at) VALUES
"""
    
    building_info = {
        247: ('247', '247号楼', '宿舍区247号', 'active', ''),
        248: ('248', '248号楼', '宿舍区248号', 'active', ''),
        249: ('249', '249号楼', '宿舍区249号', 'active', ''),
        250: ('250', '250号楼', '宿舍区250号', 'active', ''),
        99: ('99', '99号楼', '99弄（特殊）', 'active', '特殊宿舍区')
    }
    
    values = []
    for building_num in sorted(buildings):
        building_num = int(building_num)
        info = building_info.get(building_num)
        if info:
            building_no, name, address, status, remark = info
            values.append(
                f"('{building_no}', '{name}', '{address}', '{status}', '{remark}', NOW(), NOW())"
            )
    
    sql += ',\n'.join(values) + ';\n\n'
    return sql

def generate_rooms_sql(df):
    """生成房间表SQL - 匹配 rooms 表结构"""
    # 按楼号、房号、室号分组获取唯一房间
    rooms = df[['楼号', '房号', '室号', '房间', '房租']].dropna(subset=['楼号', '房号', '室号']).drop_duplicates(
        subset=['楼号', '房号', '室号']
    )
    
    sql = """-- =============================================
-- 房间管理数据导入
-- =============================================
-- 注意：需要先查询 buildings 表获取 building_id
SET @building_247 = (SELECT id FROM buildings WHERE building_no = '247' LIMIT 1);
SET @building_248 = (SELECT id FROM buildings WHERE building_no = '248' LIMIT 1);
SET @building_249 = (SELECT id FROM buildings WHERE building_no = '249' LIMIT 1);
SET @building_250 = (SELECT id FROM buildings WHERE building_no = '250' LIMIT 1);
SET @building_99 = (SELECT id FROM buildings WHERE building_no = '99' LIMIT 1);

INSERT INTO rooms (building_id, room_no, room_unit, room_name, rent_standard, electricity_price, status, remark, created_at, updated_at) VALUES
"""
    
    values = []
    for idx, row in rooms.iterrows():
        building_num = int(row['楼号'])
        room_num = int(row['房号'])
        unit_num = int(row['室号'])
        room_name = row['房间'] if pd.notna(row['房间']) else f'{room_num}室'
        rent = int(row['房租']) if pd.notna(row['房租']) else 0
        
        # 房号和室号
        room_no_str = str(room_num)
        unit_str = str(unit_num)
        
        # 默认电价
        electricity_price = "0.4900"
        
        # 备注（特殊房间）
        remark = ''
        if room_no_str in ['211', '212'] and unit_str == 'A':
            remark = '只收电费不收房租'
        
        values.append(
            f"(@building_{building_num}, '{room_no_str}', '{unit_str}', '{room_name}', "
            f"{rent}.00, {electricity_price}, 'active', '{remark}', NOW(), NOW())"
        )
    
    sql += ',\n'.join(values) + ';\n\n'
    return sql

def generate_employees_sql(df):
    """生成员工表SQL - 匹配 employees 表结构"""
    # 过滤有效的员工记录（有姓名）
    employees = df[['姓名', '任职单位', '一级部门', '职务', '转宿日期，备注']].dropna(subset=['姓名']).copy()
    
    # 去重（同一个人可能住多个房间记录）
    employees = employees.drop_duplicates(subset=['姓名'])
    
    sql = """-- =============================================
-- 员工管理数据导入
-- =============================================
INSERT INTO employees (employee_no, name, company, department, position, status, remark, created_at, updated_at) VALUES
"""
    
    values = []
    for idx, (i, row) in enumerate(employees.iterrows(), start=1001):
        name = row['姓名'].strip()
        company = row['任职单位'] if pd.notna(row['任职单位']) else '未知'
        department = row['一级部门'] if pd.notna(row['一级部门']) else '未知'
        position = row['职务'] if pd.notna(row['职务']) else '员工'
        notes = row['转宿日期，备注'] if pd.notna(row['转宿日期，备注']) else ''
        
        # 生成员工编号
        emp_number = f'EMP{idx:04d}'
        
        # 转义备注中的单引号
        notes = notes.replace("'", "''")
        
        values.append(
            f"('{emp_number}', '{name}', '{company}', '{department}', '{position}', "
            f"'active', '{notes}', NOW(), NOW())"
        )
    
    sql += ',\n'.join(values) + ';\n\n'
    return sql

def generate_residences_sql(df):
    """生成入住记录表SQL - 匹配 residence_records 表结构"""
    # 过滤有效的入住记录
    residences = df[['楼号', '房号', '室号', '姓名', '房租', '转宿日期，备注']].dropna(
        subset=['楼号', '房号', '室号', '姓名']
    ).copy()
    
    sql = """-- =============================================
-- 入住管理数据导入
-- =============================================
-- 使用临时表来处理入住记录

CREATE TEMPORARY TABLE temp_residence_data (
    building_no VARCHAR(20),
    room_no VARCHAR(50),
    room_unit VARCHAR(20),
    emp_name VARCHAR(50),
    rent_amount DECIMAL(10,2),
    is_primary_payer INT,
    probation_months INT,
    remark VARCHAR(500)
);

INSERT INTO temp_residence_data VALUES
"""
    
    temp_values = []
    for idx, row in residences.iterrows():
        building_num = int(row['楼号'])
        room_num = int(row['房号'])
        unit_num = int(row['室号'])
        name = row['姓名'].strip()
        rent = int(row['房租']) if pd.notna(row['房租']) else 0
        notes = row['转宿日期，备注'] if pd.notna(row['转宿日期，备注']) else ''
        
        # 转义备注中的单引号
        notes = notes.replace("'", "''")
        
        # 判断是否为主要缴费人（房租不为0，或没有标注夫妻间）
        is_primary = 1 if rent > 0 else 0
        if '夫妻' in notes and rent == 0:
            is_primary = 0
        
        # 判断试用期月数
        probation_months = 0
        if '试用' in notes or '前3个月' in notes or '前三个月' in notes:
            probation_months = 3
        
        temp_values.append(
            f"('{building_num}', '{room_num}', '{unit_num}', '{name}', "
            f"{rent}.00, {is_primary}, {probation_months}, '{notes}')"
        )
    
    sql += ',\n'.join(temp_values) + ';\n\n'
    
    # 使用临时表插入到正式表
    sql += """-- 从临时表插入到正式表
INSERT INTO residence_records (
    employee_id, 
    room_id, 
    check_in_date, 
    check_out_date,
    is_primary_payer,
    probation_months,
    status,
    remark,
    created_at,
    updated_at
)
SELECT 
    e.id AS employee_id,
    r.id AS room_id,
    '2024-01-01' AS check_in_date,
    NULL AS check_out_date,
    t.is_primary_payer,
    t.probation_months,
    CASE 
        WHEN t.remark LIKE '%离宿%' THEN 'invalid'
        ELSE 'valid'
    END AS status,
    t.remark,
    NOW() AS created_at,
    NOW() AS updated_at
FROM temp_residence_data t
INNER JOIN employees e ON e.name = t.emp_name
INNER JOIN rooms r ON r.room_no = t.room_no 
    AND r.room_unit = t.room_unit
INNER JOIN buildings b ON b.id = r.building_id 
    AND b.building_no = t.building_no;

-- 清理临时表
DROP TEMPORARY TABLE IF EXISTS temp_residence_data;

"""
    return sql

def main():
    """主函数"""
    # 读取Excel文件
    excel_path = Path(__file__).parent.parent / 'data' / '房间和人员数据.xlsx'
    
    print(f"正在读取文件: {excel_path}")
    df = pd.read_excel(excel_path, sheet_name='Sheet1')
    
    # 删除空行
    df = df.dropna(how='all')
    
    print(f"共读取 {len(df)} 行有效数据")
    
    # 生成输出文件
    output_file = Path(__file__).parent / 'import_all_data.sql'
    
    print(f"\n开始生成SQL文件: {output_file}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # 文件头
        f.write("""-- =============================================
-- 蓉蓉的收租小工具 - 完整数据导入脚本
-- =============================================
-- 生成时间: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """
-- 数据来源: 房间和人员数据.xlsx
-- 
-- 使用说明:
--   1. 确保已创建数据库和表结构（使用 Alembic 迁移）
--   2. 执行此脚本: mysql -u root -p dormbill < import_all_data.sql
--   3. 导入顺序: 楼栋 -> 房间 -> 员工 -> 入住记录
-- 
-- 注意事项:
--   - 本脚本会清空现有数据，请谨慎使用！
--   - 建议先备份数据库
-- =============================================

USE dormbill;

-- 清空现有数据（谨慎使用！）
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE residence_records;
TRUNCATE TABLE employees;
TRUNCATE TABLE rooms;
TRUNCATE TABLE buildings;
SET FOREIGN_KEY_CHECKS = 1;

""")
        
        # 生成楼栋SQL
        print("生成楼栋数据...")
        buildings_sql = generate_buildings_sql(df)
        f.write(buildings_sql)
        
        # 生成房间SQL
        print("生成房间数据...")
        rooms_sql = generate_rooms_sql(df)
        f.write(rooms_sql)
        
        # 生成员工SQL
        print("生成员工数据...")
        employees_sql = generate_employees_sql(df)
        f.write(employees_sql)
        
        # 生成入住记录SQL
        print("生成入住记录数据...")
        residences_sql = generate_residences_sql(df)
        f.write(residences_sql)
        
        # 文件尾 - 验证数据
        f.write("""
-- =============================================
-- 数据导入完成 - 验证统计
-- =============================================
SELECT '楼栋数量' AS 项目, COUNT(*) AS 数量 FROM buildings
UNION ALL
SELECT '房间数量', COUNT(*) FROM rooms
UNION ALL
SELECT '员工数量', COUNT(*) FROM employees
UNION ALL
SELECT '入住记录', COUNT(*) FROM residence_records;

-- 验证入住记录详情
SELECT 
    b.building_no AS 楼号,
    r.room_no AS 房号,
    r.room_unit AS 室号,
    r.room_name AS 房间名称,
    e.name AS 姓名,
    e.company AS 单位,
    e.department AS 部门,
    rr.is_primary_payer AS 主缴费人,
    rr.probation_months AS 试用期月数,
    rr.status AS 状态,
    rr.remark AS 备注
FROM residence_records rr
INNER JOIN employees e ON rr.employee_id = e.id
INNER JOIN rooms r ON rr.room_id = r.id
INNER JOIN buildings b ON r.building_id = b.id
ORDER BY b.building_no, r.room_no, r.room_unit
LIMIT 10;

SELECT '✅ 数据导入完成！请检查上面的统计信息。' AS 状态;
""")
    
    print(f"\n✅ SQL文件生成成功: {output_file}")
    print(f"\n统计信息:")
    print(f"  - 楼栋数量: {len(df['楼号'].dropna().unique())}")
    print(f"  - 房间数量: {len(df[['楼号', '房号', '室号']].dropna().drop_duplicates())}")
    print(f"  - 员工数量: {len(df['姓名'].dropna().unique())}")
    print(f"  - 入住记录: {len(df.dropna(subset=['姓名']))}")
    print(f"\n下一步:")
    print(f"  1. 确保数据库已创建并运行了 Alembic 迁移")
    print(f"  2. 备份现有数据（如有）")
    print(f"  3. 执行: mysql -u root -p dormbill < scripts/import_all_data.sql")

if __name__ == '__main__':
    main()
