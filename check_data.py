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

# 检查room_main_meter_records表中的月份
print("=== Room Main Meter Records ===")
cursor.execute("SELECT DISTINCT month FROM room_main_meter_records ORDER BY month DESC LIMIT 5")
for row in cursor.fetchall():
    print(f"Month: {row[0]}")

print("\n=== Meter Records (空调表) ===")
cursor.execute("SELECT DISTINCT month FROM meter_records ORDER BY month DESC LIMIT 5")
for row in cursor.fetchall():
    print(f"Month: {row[0]}")

print("\n=== Sample Room Main Meter Data ===")
cursor.execute("""
    SELECT m.building_id, m.room_no, m.month, m.meter_no, 
           m.previous_reading, m.current_reading, m.status
    FROM room_main_meter_records m
    ORDER BY m.month DESC, m.building_id, m.room_no
    LIMIT 3
""")
for row in cursor.fetchall():
    print(f"Building {row[0]}, Room {row[1]}, Month {row[2]}, Status {row[6]}")

cursor.close()
conn.close()
