#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成完整的入住记录导入SQL - 处理合并单元格"""

import pandas as pd
import re
import os

# 读取Excel文件
excel_file = None
for filename in os.listdir('.'):
    if '宿舍员工' in filename and filename.endswith('.xlsx'):
        excel_file = filename
        break

if not excel_file:
    print("❌ 未找到宿舍员工Excel文件")
    exit(1)

print(f"📖 读取文件: {excel_file}\n")
df = pd.read_excel(excel_file, sheet_name=0)

# 前向填充楼号和房号（处理合并单元格）
df['楼号'] = df['楼号'].fillna(method='ffill')
df['房号'] = df['房号'].fillna(method='ffill')

# 过滤出有姓名的有效行
valid_rows = df[df['姓名'].notna() & (df['姓名'] != '')]

print(f"📊 数据统计:")
print(f"   总行数: {len(df)}")
print(f"   有效记录: {len(valid_rows)}")
print(f"   有楼号: {valid_rows['楼号'].notna().sum()}")
print(f"   有房号: {valid_rows['房号'].notna().sum()}")
print(f"   有室号: {valid_rows['室号'].notna().sum()}")

# 生成SQL
sql_statements = []
sql_statements.append("-- 导入入住记录 - 完整版（处理合并单元格）")
sql_statements.append("-- 生成时间: 2026-09-11")
sql_statements.append("-- 数据来源: " + excel_file)
sql_statements.append("")

success_count = 0
skip_count = 0
skip_reasons = {}

for idx, row in valid_rows.iterrows():
    name = str(row['姓名']).strip()
    company = str(row['任职单位']).strip() if pd.notna(row['任职单位']) else ''
    
    # 房间信息
    building = row['楼号']
    room_no = row['房号']
    unit = row['室号']
    room_name = str(row['房间']).strip() if pd.notna(row['房间']) else ''
    
    # 备注
    remark = str(row['转宿日期，备注']).strip() if pd.notna(row['转宿日期，备注']) else ''
    
    # 检查必要字段
    if pd.isna(building) or pd.isna(room_no) or pd.isna(unit):
        reason = f"缺少房间信息: {building}-{room_no}-{unit}"
        skip_reasons[reason] = skip_reasons.get(reason, 0) + 1
        skip_count += 1
        sql_statements.append(f"-- 跳过: {name} ({company}) - {reason}")
        continue
    
    # 转换数据类型
    try:
        building_no = int(building)
        room_num = int(room_no)
        unit_num = int(unit)
    except:
        reason = f"房间格式错误: {building}-{room_no}-{unit}"
        skip_reasons[reason] = skip_reasons.get(reason, 0) + 1
        skip_count += 1
        sql_statements.append(f"-- 跳过: {name} ({company}) - {reason}")
        continue
    
    # 生成SQL
    sql = f"""INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    {f"'{remark}'" if remark and remark != 'nan' else 'NULL'},
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '{building_no}')
WHERE e.name = '{name}'
  AND e.company = '{company}'
  AND r.room_no = '{room_num}'
  AND r.room_unit = '{unit_num}'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;
"""
    sql_statements.append(sql)
    success_count += 1

# 输出到文件
output_file = 'scripts/import_residence_records_complete.sql'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(sql_statements))

print(f"\n✅ SQL生成完成:")
print(f"   成功: {success_count}条")
print(f"   跳过: {skip_count}条")
print(f"   输出文件: {output_file}")

if skip_reasons:
    print(f"\n⚠️  跳过原因统计:")
    for reason, count in skip_reasons.items():
        print(f"   {reason}: {count}条")
