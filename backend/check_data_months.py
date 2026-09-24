"""检查数据库中有数据的月份"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from datetime import date
from app.database import SessionLocal
from app.models.room_main_meter import RoomMainMeterRecord
from app.models.water import WaterMeterRecord
from sqlalchemy import func

def check_data_months():
    """检查数据库中有数据的月份"""
    db = SessionLocal()
    
    try:
        print("\n检查数据库中的电表和水表数据...")
        
        # 检查总表数据
        main_meter_months = db.query(
            RoomMainMeterRecord.month,
            func.count(RoomMainMeterRecord.id).label('count')
        ).group_by(RoomMainMeterRecord.month).all()
        
        print("\n【总表数据】")
        if main_meter_months:
            for month, count in main_meter_months:
                print(f"  {month}: {count} 条记录")
        else:
            print("  无数据")
        
        # 检查水表数据
        water_meter_months = db.query(
            WaterMeterRecord.month,
            func.count(WaterMeterRecord.id).label('count')
        ).group_by(WaterMeterRecord.month).all()
        
        print("\n【水表数据】")
        if water_meter_months:
            for month, count in water_meter_months:
                print(f"  {month}: {count} 条记录")
        else:
            print("  无数据")
        
        # 如果有数据，使用最新的月份进行测试
        if main_meter_months:
            latest_month = max(month for month, _ in main_meter_months)
            print(f"\n建议使用月份: {latest_month}")
            return latest_month
        
    finally:
        db.close()
    
    return None


if __name__ == "__main__":
    check_data_months()
