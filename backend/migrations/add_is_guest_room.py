"""添加房间客房标识字段"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy import text
from app.database import engine

def migrate():
    sql = text("""
    ALTER TABLE rooms 
    ADD COLUMN is_guest_room TINYINT(1) DEFAULT 0 COMMENT '是否为客房（客房水电租全免）' AFTER rent_standard
    """)
    
    index_sql = text("""
    CREATE INDEX idx_is_guest_room ON rooms(is_guest_room)
    """)
    
    with engine.connect() as conn:
        try:
            conn.execute(sql)
            print("✓ 添加 is_guest_room 字段成功")
        except Exception as e:
            if "Duplicate column name" in str(e):
                print("✓ is_guest_room 字段已存在，跳过")
            else:
                print(f"✗ 添加字段失败: {e}")
                raise
        
        try:
            conn.execute(index_sql)
            print("✓ 创建索引成功")
        except Exception as e:
            if "Duplicate key name" in str(e):
                print("✓ 索引已存在，跳过")
            else:
                print(f"✗ 创建索引失败: {e}")
        
        conn.commit()
        print("\n数据库迁移完成！")

if __name__ == "__main__":
    migrate()
