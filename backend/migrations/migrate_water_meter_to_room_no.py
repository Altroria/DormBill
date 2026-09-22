"""
迁移水表记录表：从按room_id改为按room_no
"""
from sqlalchemy import text
from app.database import engine


def migrate():
    """执行迁移"""
    with engine.connect() as conn:
        # 1. 添加 room_no 列（如果不存在）
        try:
            conn.execute(text("""
                ALTER TABLE water_meter_records 
                ADD COLUMN room_no VARCHAR(50) AFTER building_id
            """))
            conn.commit()
            print("✓ 添加 room_no 列")
        except Exception as e:
            if "Duplicate column name" in str(e):
                print("✓ room_no 列已存在")
            else:
                raise
        
        # 2. 从现有数据填充 room_no（如果有旧数据）
        result = conn.execute(text("""
            UPDATE water_meter_records wmr
            JOIN rooms r ON wmr.room_id = r.id
            SET wmr.room_no = r.room_no
            WHERE wmr.room_no IS NULL
        """))
        conn.commit()
        print(f"✓ 更新了 {result.rowcount} 条记录的 room_no")
        
        # 3. 删除旧的唯一索引 uk_room_month
        try:
            conn.execute(text("""
                ALTER TABLE water_meter_records 
                DROP INDEX uk_room_month
            """))
            conn.commit()
            print("✓ 删除旧唯一索引 uk_room_month")
        except Exception as e:
            if "check that it exists" in str(e) or "Can't DROP" in str(e):
                print("✓ 旧唯一索引已删除")
            else:
                raise
        
        # 4. 删除外键约束
        try:
            conn.execute(text("""
                ALTER TABLE water_meter_records 
                DROP FOREIGN KEY water_meter_records_ibfk_1
            """))
            conn.commit()
            print("✓ 删除外键约束")
        except Exception as e:
            if "check that" in str(e).lower() or "cannot drop" in str(e).lower():
                print("✓ 外键约束已删除")
            else:
                raise
        
        # 5. 删除 room_id 列
        try:
            conn.execute(text("""
                ALTER TABLE water_meter_records 
                DROP COLUMN room_id
            """))
            conn.commit()
            print("✓ 删除 room_id 列")
        except Exception as e:
            if "Can't DROP" in str(e):
                print("✓ room_id 列已删除")
            else:
                raise
        
        # 6. 添加唯一索引（building_id, room_no, month）
        try:
            conn.execute(text("""
                ALTER TABLE water_meter_records 
                ADD UNIQUE INDEX idx_building_room_month (building_id, room_no, month)
            """))
            conn.commit()
            print("✓ 添加唯一索引")
        except Exception as e:
            if "Duplicate key name" in str(e):
                print("✓ 唯一索引已存在")
            else:
                raise
        
        print("\n迁移完成！")


if __name__ == "__main__":
    migrate()
