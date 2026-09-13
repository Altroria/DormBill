import pymysql
import os
from dotenv import load_dotenv

load_dotenv('backend/.env')

conn = pymysql.connect(
    host=os.getenv('DB_HOST', 'localhost'),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME', 'dormbill'),
    charset='utf8mb4'
)

cursor = conn.cursor()

# 检查表是否存在
print("=== Check Tables ===")
cursor.execute("SHOW TABLES LIKE 'room_main_meter_records'")
result = cursor.fetchone()
if result:
    print(f"Table exists: {result[0]}")
    cursor.execute("DESCRIBE room_main_meter_records")
    print("\nTable structure:")
    for row in cursor.fetchall():
        print(f"  {row[0]} - {row[1]}")
    
    cursor.execute("SELECT COUNT(*) FROM room_main_meter_records")
    count = cursor.fetchone()[0]
    print(f"\nTotal records: {count}")
else:
    print("Table does NOT exist!")

print("\n=== Check meter_records ===")
cursor.execute("SELECT COUNT(*) FROM meter_records WHERE month = '2026-09-01'")
count = cursor.fetchone()[0]
print(f"Meter records for 2026-09: {count}")

cursor.execute("""
    SELECT m.id, m.room_id, r.room_no, m.month, m.ac_previous_reading, m.ac_current_reading
    FROM meter_records m
    JOIN rooms r ON m.room_id = r.id
    WHERE m.month = '2026-09-01'
    LIMIT 3
""")
print("\nSample records:")
for row in cursor.fetchall():
    print(f"  Room {row[2]}, Month {row[3]}, Readings: {row[4]} -> {row[5]}")

cursor.close()
conn.close()
