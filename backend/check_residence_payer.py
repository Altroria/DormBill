"""检查入住记录的主缴费人标记"""
from app.database import engine
from sqlalchemy import text

conn = engine.connect()

# 检查入住记录中 is_primary_payer 的分布
result = conn.execute(text("""
    SELECT 
        r.id, 
        e.name as employee_name,
        e.employee_no,
        r.is_primary_payer,
        r.check_in_date,
        r.check_out_date,
        r.status,
        rm.room_name,
        rm.rent_standard
    FROM residence_records r
    JOIN employees e ON r.employee_id = e.id
    JOIN rooms rm ON r.room_id = rm.id
    WHERE r.status != 'invalid'
    ORDER BY r.is_primary_payer, e.name
    LIMIT 50
"""))

print("=" * 100)
print("入住记录样本（按主缴费人分组）:")
print("=" * 100)
print(f"{'ID':<6} {'员工':<12} {'工号':<10} {'主缴费人':<10} {'入住日期':<12} {'搬离日期':<12} {'房间':<20} {'房租标准':<10}")
print("-" * 100)

for row in result:
    check_out = str(row.check_out_date) if row.check_out_date else "未搬离"
    payer_status = "是(1)" if row.is_primary_payer == 1 else "否(0)" if row.is_primary_payer == 0 else f"未知({row.is_primary_payer})"
    print(f"{row.id:<6} {row.employee_name:<12} {row.employee_no:<10} {payer_status:<10} {str(row.check_in_date):<12} {check_out:<12} {row.room_name:<20} {row.rent_standard:<10}")

# 统计分布
print("\n" + "=" * 100)
print("统计汇总:")
print("=" * 100)

stats = conn.execute(text("""
    SELECT 
        is_primary_payer,
        COUNT(*) as count
    FROM residence_records
    WHERE status != 'invalid'
    GROUP BY is_primary_payer
"""))

for row in stats:
    payer_label = "主缴费人" if row.is_primary_payer == 1 else "非主缴费人(配偶)" if row.is_primary_payer == 0 else f"未知值({row.is_primary_payer})"
    print(f"{payer_label}: {row.count} 条记录")

conn.close()
