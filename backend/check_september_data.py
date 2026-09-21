"""检查9月份的电表数据"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.config import settings
from datetime import date

# 创建数据库连接
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

# 检查9月份的电表数据
month = date(2026, 9, 1)

print("=== 检查2026年9月电表数据 ===\n")

# 1. 检查主电表记录
query = text("""
SELECT COUNT(*) as count, 
       SUM(CASE WHEN total_degree > 0 THEN 1 ELSE 0 END) as with_degree,
       SUM(CASE WHEN total_fee > 0 THEN 1 ELSE 0 END) as with_fee
FROM meter_records 
WHERE month = '2026-09-01'
""")
result = db.execute(query).fetchone()
print(f"主电表记录:")
print(f"  总记录数: {result[0]}")
print(f"  有用电量的: {result[1]}")
print(f"  有总电费的: {result[2]}\n")

# 2. 检查空调数据（使用 meter_records 中的 ac_ 字段）
query = text("""
SELECT COUNT(*) as count,
       SUM(CASE WHEN ac_degree > 0 THEN 1 ELSE 0 END) as with_degree,
       SUM(CASE WHEN ac_fee > 0 THEN 1 ELSE 0 END) as with_fee
FROM meter_records
WHERE month = '2026-09-01'
""")
result = db.execute(query).fetchone()
print(f"空调电表记录:")
print(f"  总记录数: {result[0]}")
print(f"  有用电量的: {result[1]}")
print(f"  有总电费的: {result[2]}\n")

# 3. 显示几条主电表记录样例
query = text("""
SELECT r.building_id, r.room_no, mr.previous_reading, mr.current_reading, 
       mr.total_degree, mr.total_fee
FROM meter_records mr
JOIN rooms r ON mr.room_id = r.id
WHERE mr.month = '2026-09-01'
ORDER BY mr.total_fee DESC
LIMIT 5
""")
print("主电表记录样例（前5条，按电费降序）:")
results = db.execute(query).fetchall()
for row in results:
    print(f"  楼栋{row[0]} 房间{row[1]}: 上月{row[2]} -> 本月{row[3]}, 用电{row[4]}度, 电费¥{row[5]}")

# 4. 显示几条空调电表记录样例
query = text("""
SELECT r.building_id, r.room_no, mr.ac_previous_reading, mr.ac_current_reading,
       mr.ac_degree, mr.ac_fee
FROM meter_records mr
JOIN rooms r ON mr.room_id = r.id
WHERE mr.month = '2026-09-01' AND mr.ac_fee > 0
ORDER BY mr.ac_fee DESC
LIMIT 5
""")
print("\n空调电表记录样例（前5条，按空调费降序）:")
results = db.execute(query).fetchall()
if results:
    for row in results:
        print(f"  楼栋{row[0]} 房间{row[1]}: 上月{row[2]} -> 本月{row[3]}, 用电{row[4]}度, 电费¥{row[5]}")
else:
    print("  没有空调电表记录")

db.close()
