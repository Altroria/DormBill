"""验证房租计算是否正常"""
from app.database import SessionLocal
from app.services.rent_service import calculate_rent_actual_with_overrides
from app.models.residence import ResidenceRecord
from app.models.room import Room
from app.models.employee import Employee
from datetime import date
from decimal import Decimal

db = SessionLocal()

try:
    # 测试月份
    target_month = date(2026, 9, 1)
    
    print("=" * 100)
    print(f"测试房租计算 - {target_month.year}年{target_month.month}月")
    print("=" * 100)
    
    # 随机抽取10个入住记录测试
    residences = db.query(ResidenceRecord).filter(
        ResidenceRecord.status != "invalid"
    ).limit(10).all()
    
    print(f"{'员工':<12} {'工号':<12} {'房间':<20} {'房租标准':<10} {'主缴费人':<10} {'计算房租':<10}")
    print("-" * 100)
    
    for res in residences:
        room = db.query(Room).filter(Room.id == res.room_id).first()
        emp = db.query(Employee).filter(Employee.id == res.employee_id).first()
        
        if not room or not emp:
            continue
        
        rent_standard = Decimal(str(room.rent_standard))
        rent_actual = calculate_rent_actual_with_overrides(
            res, rent_standard, target_month
        )
        
        payer_status = "是(1)" if res.is_primary_payer == 1 else "否(0)"
        
        print(f"{emp.name:<12} {emp.employee_no:<12} {room.room_name:<20} ¥{rent_standard:<9} {payer_status:<10} ¥{rent_actual}")
    
    print("\n" + "=" * 100)
    print("结论:")
    print("=" * 100)
    
    # 统计所有人的房租
    all_residences = db.query(ResidenceRecord).filter(
        ResidenceRecord.status != "invalid"
    ).all()
    
    zero_rent_count = 0
    has_rent_count = 0
    
    for res in all_residences:
        room = db.query(Room).filter(Room.id == res.room_id).first()
        if not room:
            continue
        
        rent_standard = Decimal(str(room.rent_standard))
        rent_actual = calculate_rent_actual_with_overrides(
            res, rent_standard, target_month
        )
        
        if rent_actual == Decimal("0"):
            zero_rent_count += 1
        else:
            has_rent_count += 1
    
    print(f"有房租的记录: {has_rent_count} 条")
    print(f"房租为0的记录: {zero_rent_count} 条")
    print(f"总记录数: {len(all_residences)} 条")
    
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
