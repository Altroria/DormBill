"""检查房间表的status字段 - MySQL版本"""
from app.database import engine
from sqlalchemy import text

conn = engine.connect()

# 检查字段定义（包括enum值）
result = conn.execute(text("""
    SELECT COLUMN_TYPE 
    FROM information_schema.COLUMNS 
    WHERE TABLE_SCHEMA = 'dormbill' 
    AND TABLE_NAME = 'rooms' 
    AND COLUMN_NAME = 'status'
"""))

print("房间表status字段定义:")
for row in result:
    print(f"  {row[0]}")

conn.close()
