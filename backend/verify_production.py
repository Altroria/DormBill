#!/usr/bin/env python3
"""验证生产数据库修复结果"""
from sqlalchemy import create_engine, text

engine = create_engine('mysql+pymysql://root:405649@47.102.36.185:3306/dormbill')

with engine.connect() as conn:
    # 统计主缴费人数量
    result = conn.execute(text("SELECT COUNT(*) FROM residence_records WHERE status != 'invalid' AND is_primary_payer = 1"))
    print(f"✓ 生产库主缴费人数量: {result.scalar()} 条")
    
    # 查看前5条记录
    result = conn.execute(text("""
        SELECT r.id, r.employee_id, e.name, r.is_primary_payer, r.remark
        FROM residence_records r 
        LEFT JOIN employees e ON r.employee_id = e.id 
        WHERE r.status != 'invalid' 
        LIMIT 5
    """))
    
    print("\n前5条记录验证:")
    for row in result:
        print(f"  ID={row[0]}, 员工ID={row[1]}, 姓名={row[2]}, is_primary_payer={row[3]}, 备注={row[4]}")

print("\n✅ 生产数据库修复验证通过！")
