"""检查非主缴费人的备注信息"""
from app.database import engine
from sqlalchemy import text

conn = engine.connect()

# 检查非主缴费人的备注
result = conn.execute(text("""
    SELECT 
        r.id,
        e.name,
        e.employee_no,
        r.is_primary_payer,
        r.remark,
        rm.room_name
    FROM residence_records r
    JOIN employees e ON r.employee_id = e.id
    JOIN rooms rm ON r.room_id = rm.id
    WHERE r.status != 'invalid' AND r.is_primary_payer = 0
    LIMIT 20
"""))

print("=" * 100)
print("非主缴费人样本（is_primary_payer=0）:")
print("=" * 100)

for row in result:
    print(f"员工: {row.name} ({row.employee_no})")
    print(f"  is_primary_payer = {row.is_primary_payer}")
    print(f"  remark = \"{row.remark}\"")
    print(f"  房间 = {row.room_name}")
    print()

# 检查主缴费人的备注
print("=" * 100)
print("主缴费人样本（is_primary_payer=1）:")
print("=" * 100)

result2 = conn.execute(text("""
    SELECT 
        r.id,
        e.name,
        e.employee_no,
        r.is_primary_payer,
        r.remark,
        rm.room_name
    FROM residence_records r
    JOIN employees e ON r.employee_id = e.id
    JOIN rooms rm ON r.room_id = rm.id
    WHERE r.status != 'invalid' AND r.is_primary_payer = 1
    LIMIT 20
"""))

for row in result2:
    print(f"员工: {row.name} ({row.employee_no})")
    print(f"  is_primary_payer = {row.is_primary_payer}")
    print(f"  remark = \"{row.remark}\"")
    print(f"  房间 = {row.room_name}")
    print()

conn.close()
