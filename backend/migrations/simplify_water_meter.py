"""
简化水费管理 - 删除不需要的字段
只保留：building_id, room_no, month, total_fee, remark
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import text
from app.database import engine


def migrate():
    """执行数据库迁移"""
    
    with engine.connect() as conn:
        print("开始迁移：简化水费管理表结构")
        
        # 1. 先查询表结构，确认字段是否存在
        result = conn.execute(text("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = DATABASE() 
            AND TABLE_NAME = 'water_meter_records'
        """))
        existing_columns = {row[0] for row in result}
        
        # 2. 删除不需要的字段
        columns_to_drop = [
            'water_meter_no',
            'previous_reading', 
            'current_reading',
            'usage',
            'unit_price',
            'status',
        ]
        
        for column in columns_to_drop:
            if column in existing_columns:
                try:
                    print(f"  删除字段: {column}")
                    # 使用反引号处理保留字
                    conn.execute(text(f"ALTER TABLE water_meter_records DROP COLUMN `{column}`"))
                    conn.commit()
                    print(f"    ✓ 已删除")
                except Exception as e:
                    print(f"    × 失败: {e}")
                    conn.rollback()
            else:
                print(f"  跳过字段: {column} (不存在)")
        
        print("\n✓ 迁移完成！")
        print("\n保留的字段:")
        print("  - id")
        print("  - building_id")
        print("  - room_no")
        print("  - month")
        print("  - total_fee (水费)")
        print("  - remark (备注)")
        print("  - created_at")
        print("  - updated_at")


if __name__ == "__main__":
    migrate()
