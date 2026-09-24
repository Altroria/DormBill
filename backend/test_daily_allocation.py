"""测试按天分摊逻辑"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from datetime import date
from decimal import Decimal
from app.database import SessionLocal
from app.services.electricity_calculation_service import ElectricityCalculationService
from app.services.water_meter_service import get_employee_water_fee_for_month
from app.models import ResidenceRecord, Room, Employee
from sqlalchemy import and_

def test_daily_allocation():
    """测试按天分摊"""
    db = SessionLocal()
    
    try:
        print("\n" + "="*60)
        print("测试按天分摊逻辑")
        print("="*60)
        
        target_month = date(2026, 9, 1)  # 使用2026年9月
        
        # 1. 测试电费分摊
        print("\n【电费分摊测试】")
        print("-"*60)
        
        calc_service = ElectricityCalculationService(db)
        
        # 查询一个有数据的房号
        from app.models.room_main_meter import RoomMainMeterRecord
        main_meters = db.query(RoomMainMeterRecord).filter(
            RoomMainMeterRecord.month == target_month
        ).limit(3).all()
        
        if not main_meters:
            print("⚠️  没有找到电表记录")
        
        for main_meter in main_meters:
            try:
                result = calc_service.calculate_room_no_electricity(
                    building_id=main_meter.building_id,
                    room_no=main_meter.room_no,
                    month=target_month,
                )
                
                print(f"\n房号: {result['room_no']}")
                print(f"公共电费总额: {result['common_fee']:.2f} 元")
                print(f"空调电费总额: {result['total_ac_fee']:.2f} 元")
                print(f"入住总人天数: {result['total_stay_days']}")
                print(f"入住总人数: {result['total_occupants']}")
                
                if result['distributions']:
                    print("\n个人分摊明细:")
                    print(f"{'员工ID':<10} {'入住天数':<10} {'公共电费':<12} {'空调电费':<12} {'总电费':<12}")
                    print("-" * 60)
                    
                    for dist in result['distributions']:
                        emp = db.query(Employee).filter(Employee.id == dist['employee_id']).first()
                        emp_name = emp.name if emp else "未知"
                        
                        print(f"{dist['employee_id']:<10} {dist['stay_days']:<10} "
                              f"{dist['common_electricity_fee']:<12.2f} "
                              f"{dist['ac_electricity_fee']:<12.2f} "
                              f"{dist['total_electricity_fee']:<12.2f} ({emp_name})")
                    
                    # 验证总和
                    total_common = sum(Decimal(str(d['common_electricity_fee'])) for d in result['distributions'])
                    total_ac = sum(Decimal(str(d['ac_electricity_fee'])) for d in result['distributions'])
                    print(f"\n验证: 公共电费总和 = {float(total_common):.2f} (应为 {result['common_fee']:.2f})")
                    print(f"验证: 空调电费总和 = {float(total_ac):.2f} (应为 {result['total_ac_fee']:.2f})")
                    
            except Exception as e:
                print(f"❌ 房号 {main_meter.room_no} 计算失败: {e}")
        
        # 2. 测试水费分摊
        print("\n\n【水费分摊测试】")
        print("-"*60)
        
        # 查询几个有入住记录的员工
        residences = db.query(ResidenceRecord).filter(
            ResidenceRecord.status.in_(["valid", "leave"])
        ).limit(5).all()
        
        if not residences:
            print("⚠️  没有找到入住记录")
        
        for res in residences:
            emp = db.query(Employee).filter(Employee.id == res.employee_id).first()
            room = db.query(Room).filter(Room.id == res.room_id).first()
            
            if not emp or not room:
                continue
            
            water_fee = get_employee_water_fee_for_month(db, emp.id, target_month)
            
            from app.utils.date_utils import stay_days_in_month
            stay_days = stay_days_in_month(res.check_in_date, res.check_out_date, target_month)
            
            print(f"\n员工: {emp.name} (ID: {emp.id})")
            print(f"房间: {room.room_no}-{room.room_name}")
            print(f"状态: {res.status}")
            print(f"入住日期: {res.check_in_date}")
            print(f"搬离日期: {res.check_out_date or '未搬离'}")
            print(f"当月入住天数: {stay_days} 天")
            print(f"分摊水费: {float(water_fee):.2f} 元")
        
        print("\n" + "="*60)
        print("✅ 测试完成")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    test_daily_allocation()
