#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提取并生成女生宿舍员工导入SQL
"""

import pandas as pd
from datetime import datetime

# 读取Excel
df = pd.read_excel('7月宿舍员工 扣款.xlsx', header=0)

# 前向填充楼号和房号
df['楼号'] = df['楼号'].ffill()
df['房号'] = df['房号'].ffill()

# 只保留有姓名的行
df = df[df['姓名'].notna()].copy()

# 筛选女生宿舍记录
female_dorm = df[df['房号'].astype(str).str.contains('女生宿舍', na=False)].copy()

print(f"📊 女生宿舍总人数: {len(female_dorm)}")

# 提取唯一员工
employees = []
for idx, row in female_dorm.iterrows():
    name = row['姓名']
    company = row['任职单位'] if pd.notna(row['任职单位']) else '未知'
    
    # 去重
    if not any(e['name'] == name and e['company'] == company for e in employees):
        employees.append({
            'name': name,
            'company': company
        })

print(f"👥 唯一员工数: {len(employees)}")

# 生成SQL
sql_lines = [
    "-- 女生宿舍员工导入",
    f"-- 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    f"-- 员工数量: {len(employees)}",
    "",
]

for emp in employees:
    name = emp['name']
    company = emp['company']
    
    sql = f"""INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '{name}', '{company}', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '{name}' AND company = '{company}'
);
"""
    sql_lines.append(sql)

# 写入文件
output_file = 'scripts/import_female_dorm_employees.sql'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(sql_lines))

print(f"\n✅ 生成SQL: {output_file}")
print(f"📝 包含 {len(employees)} 名员工")

# 显示员工列表
print("\n👥 员工列表（按公司分组）:")
employees_by_company = {}
for emp in employees:
    company = emp['company']
    if company not in employees_by_company:
        employees_by_company[company] = []
    employees_by_company[company].append(emp['name'])

for company, names in sorted(employees_by_company.items()):
    print(f"\n  {company} ({len(names)}人):")
    for name in names:
        print(f"    - {name}")
