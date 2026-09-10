#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成入住管理数据的SQL脚本
从Excel文件读取员工和房间信息，生成residences表的INSERT语句
"""

import openpyxl
import glob
from datetime import datetime

def main():
    # 查找Excel文件
    excel_files = glob.glob('7月*.xlsx')
    
    if not excel_files:
        print("错误：未找到7月开头的Excel文件")
        return
    
    # 读取员工扣款文件
    employee_file = None
    for f in excel_files:
        if '员工' in f or '扣款' in f:
            employee_file = f
            break
    
    if not employee_file:
        print("错误：未找到员工扣款文件")
        return
    
    print(f"读取文件: {employee_file}")
    
    try:
        wb = openpyxl.load_workbook(employee_file, read_only=True)
        sheet = wb.active
        
        # 读取数据并生成SQL
        sql_statements = []
        sql_statements.append("-- 入住管理数据")
        sql_statements.append("-- 生成时间: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        sql_statements.append("-- 数据来源: " + employee_file)
        sql_statements.append("")
        
        # 收集所有入住记录
        residences = []
        current_building = None
        current_room_no = None
        
        for row in sheet.iter_rows(min_row=3, values_only=True):
            building_no = row[0]  # 楼号
            room_no = row[1]      # 房号
            room_suffix = row[4]  # 室号
            room_name = row[5]    # 房间
            company = row[6]      # 任职单位
            department = row[7]   # 一级部门
            position = row[8]     # 职务
            name = row[9]         # 姓名
            remark = row[10]      # 转宿日期，备注
            
            # 跳过空行
            if not name:
                continue
            
            # 更新当前楼栋和房间号
            if building_no:
                # 处理楼号，可能是数字或者范围
                building_str = str(building_no).split('-')[0].strip()
                try:
                    current_building = int(building_str)
                except:
                    current_building = building_str
            if room_no:
                # 处理房间号，可能包含中文注释
                room_no_str = str(room_no).split('（')[0].split('(')[0].strip()
                try:
                    current_room_no = str(int(room_no_str))
                except:
                    current_room_no = room_no_str
            
            # 构建完整房间号
            if current_building and current_room_no:
                full_room_no = f"{current_building}-{current_room_no}"
                if room_suffix:
                    full_room_no += f"-{room_suffix}"
                
                residences.append({
                    'name': name,
                    'company': company,
                    'department': department,
                    'position': position,
                    'room_no': full_room_no,
                    'room_name': room_name,
                    'remark': remark if remark else None
                })
        
        wb.close()
        
        print(f"\n找到 {len(residences)} 条入住记录")
        
        # 生成SQL INSERT语句
        sql_statements.append("-- 入住记录")
        sql_statements.append("-- 注意：此SQL需要先导入员工和房间数据后才能执行")
        sql_statements.append("-- 使用子查询匹配employee_id和room_id")
        sql_statements.append("")
        sql_statements.append("INSERT INTO residence_records (employee_id, room_id, check_in_date, check_out_date, status, remark)")
        sql_statements.append("VALUES")
        
        insert_values = []
        for i, res in enumerate(residences):
            # 查找employee_id - 使用姓名和公司精确匹配
            name_escaped = res['name'].replace("'", "''")
            company_escaped = res['company'].replace("'", "''") if res['company'] else ''
            
            employee_query = f"(SELECT id FROM employees WHERE name = '{name_escaped}'"
            if res['company']:
                employee_query += f" AND company = '{company_escaped}'"
            employee_query += " LIMIT 1)"
            
            # 查找room_id - 使用building_id和room_no组合匹配
            # 从完整房间号中提取楼栋号和房间号
            room_parts = res['room_no'].split('-')
            if len(room_parts) >= 2:
                building_no = room_parts[0]
                room_number = room_parts[1]
                
                # 使用building_id和room_no精确匹配
                room_query = f"(SELECT r.id FROM rooms r JOIN buildings b ON r.building_id = b.id WHERE b.building_no = '{building_no}' AND r.room_no = '{room_number}' LIMIT 1)"
            else:
                # 如果格式不对，使用房间名称匹配
                room_name_escaped = res['room_name'].replace("'", "''") if res['room_name'] else ''
                room_query = f"(SELECT id FROM rooms WHERE room_name = '{room_name_escaped}' LIMIT 1)"
            
            remark_escaped = res['remark'].replace("'", "''") if res['remark'] else None
            remark_value = f"'{remark_escaped}'" if remark_escaped else 'NULL'
            
            value = f"  ({employee_query}, {room_query}, '2026-07-01', NULL, 'valid', {remark_value})"
            insert_values.append(value)
        
        sql_statements.append(',\n'.join(insert_values) + ';')
        sql_statements.append("")
        
        # 保存SQL文件
        output_file = 'scripts/import_residences.sql'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(sql_statements))
        
        print(f"\nSQL文件已生成: {output_file}")
        print(f"共生成 {len(residences)} 条INSERT语句")
        
        # 显示前5条记录
        print("\n前5条记录示例:")
        for res in residences[:5]:
            print(f"  {res['name']} ({res['company']}) -> {res['room_no']} {res['room_name']}")
        
    except Exception as e:
        print(f"处理失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
