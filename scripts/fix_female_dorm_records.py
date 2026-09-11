#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复版：生成女生宿舍入住记录SQL
修复点：
1. 室号从1.0改为1（整数格式）
2. 房间号使用LIKE匹配（因为数据库中是"401（女生宿舍）"）
"""

import pandas as pd
import re
from datetime import datetime

# 读取Excel
df = pd.read_excel('7月宿舍员工 扣款.xlsx', header=0)

# 前向填充楼号和房号
df['楼号'] = df['楼号'].ffill()
df['房号'] = df['房号'].ffill()

# 只保留有姓名的行
df = df[df['姓名'].notna()].copy()

print(f"📊 总记录数: {len(df)}")

# 识别特殊格式的房间号
special_rooms = []
for idx, row in df.iterrows():
    building_no = str(row['楼号']) if pd.notna(row['楼号']) else ''
    room_no = str(row['房号']) if pd.notna(row['房号']) else ''
    room_unit = str(row['室号']) if pd.notna(row['室号']) else ''
    name = row['姓名']
    company = row['任职单位'] if pd.notna(row['任职单位']) else '未知'
    room_name = row['房间'] if pd.notna(row['房间']) else ''
    
    # 检查是否包含"女生宿舍"
    if '女生宿舍' in room_no or '女生宿舍' in building_no:
        # 清洗房号：提取纯数字部分
        clean_room = re.sub(r'[（(].*?[)）]', '', room_no).strip()
        
        # 清洗室号：从1.0变成1
        clean_unit = room_unit.replace('.0', '').strip()
        
        special_rooms.append({
            '原房号': room_no,
            '清洗后房号': clean_room,
            '原室号': room_unit,
            '清洗后室号': clean_unit,
            '姓名': name,
            '公司': company,
            '房间名称': room_name
        })

print(f"🏠 女生宿舍记录: {len(special_rooms)}条\n")

# 生成SQL
sql_lines = [
    "-- 女生宿舍入住记录导入（修复版）",
    f"-- 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    "-- 修复点：",
    "-- 1. 室号格式：1.0 -> 1",
    "-- 2. 房间号匹配：使用LIKE '401%'匹配'401（女生宿舍）'",
    ""
]

success_count = 0
skipped_records = []

for room in special_rooms:
    room_no = room['清洗后房号']
    room_unit = room['清洗后室号']
    name = room['姓名']
    company = room['公司']
    
    # 跳过无效数据
    if not room_no or room_no == 'nan' or not room_unit or room_unit == 'nan':
        skipped_records.append(f"房号或室号为空: {name} ({company})")
        continue
    
    # 生成INSERT语句 - 使用LIKE匹配房间号
    sql = f"""
INSERT INTO residence_records (employee_id, room_id, check_in_date, remark, created_at, updated_at)
SELECT 
    e.id,
    r.id,
    '2024-07-01',
    '女生宿舍',
    NOW(),
    NOW()
FROM employees e
JOIN rooms r ON r.building_id = (SELECT id FROM buildings WHERE building_no = '250')
WHERE e.name = '{name}'
  AND e.company = '{company}'
  AND r.room_no LIKE '{room_no}%'
  AND r.room_unit = '{room_unit}'
  AND NOT EXISTS (
      SELECT 1 FROM residence_records rr2 
      WHERE rr2.employee_id = e.id AND rr2.room_id = r.id
  )
LIMIT 1;
"""
    sql_lines.append(sql)
    success_count += 1

# 写入SQL文件
output_file = 'scripts/import_female_dorm_records_fixed.sql'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(sql_lines))

print(f"✅ 生成SQL: {success_count}条")
print(f"📝 输出文件: {output_file}")

if skipped_records:
    print(f"\n⚠️  跳过 {len(skipped_records)} 条:")
    for record in skipped_records[:10]:
        print(f"   - {record}")

# 显示示例
print("\n📋 数据示例（前5条）:")
print("-" * 80)
for i, room in enumerate(special_rooms[:5], 1):
    print(f"{i}. {room['姓名']:8s} ({room['公司']:6s}) | {room['原房号']:20s} -> {room['清洗后房号']:6s} | 室号: {room['原室号']:6s} -> {room['清洗后室号']:3s}")
