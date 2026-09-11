#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""分析入住记录缺失数据 - 改进版"""

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

# 找到姓名列
name_col = '姓名'
if name_col not in df.columns:
    print("❌ 未找到姓名列")
    exit(1)

# 过滤出有姓名的行
valid_rows = df[df[name_col].notna() & (df[name_col] != '')]
print(f"📊 Excel统计:")
print(f"   总行数: {len(df)}")
print(f"   有姓名的行: {len(valid_rows)}")

# 分析楼号、房号、室号
print(f"\n🏠 房间信息分析:")
has_building = valid_rows['楼号'].notna().sum()
has_room = valid_rows['房号'].notna().sum()
has_unit = valid_rows['室号'].notna().sum()
has_room_name = valid_rows['房间'].notna().sum()

print(f"   有楼号: {has_building}人")
print(f"   有房号: {has_room}人")
print(f"   有室号: {has_unit}人")
print(f"   有房间名称: {has_room_name}人")

# 显示前20行的关键信息
print(f"\n📋 前20条记录:")
print("-" * 100)
for idx, row in valid_rows.head(20).iterrows():
    building = row['楼号'] if pd.notna(row['楼号']) else '无'
    room = row['房号'] if pd.notna(row['房号']) else '无'
    unit = row['室号'] if pd.notna(row['室号']) else '无'
    room_name = row['房间'] if pd.notna(row['房间']) else '无'
    company = row['任职单位'] if pd.notna(row['任职单位']) else '无'
    name = row['姓名']
    
    print(f"{idx:3d}. {name:8s} | {company:8s} | {building}-{room}-{unit} | {room_name}")

# 统计公司分布
print(f"\n🏢 公司分布:")
companies = valid_rows['任职单位'].value_counts()
for company, count in companies.items():
    print(f"   {company}: {count}人")

# 统计缺失楼号的记录
missing_building = valid_rows[valid_rows['楼号'].isna()]
if len(missing_building) > 0:
    print(f"\n⚠️  缺少楼号的记录 ({len(missing_building)}人):")
    for idx, row in missing_building.iterrows():
        name = row['姓名']
        company = row['任职单位'] if pd.notna(row['任职单位']) else '无'
        room_name = row['房间'] if pd.notna(row['房间']) else '无'
        print(f"   {name} ({company}) - {room_name}")
