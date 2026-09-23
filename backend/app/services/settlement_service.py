"""结算服务：生成月度最终扣款"""
from decimal import Decimal
from datetime import date
from typing import List, Dict
from sqlalchemy.orm import Session
from sqlalchemy import and_

from ..models import (
    MonthlySettlement, MeterRecord, ResidenceRecord, Room, Employee, Building,
)
from ..models.room_main_meter import RoomMainMeterRecord
from ..utils.date_utils import month_start, month_end
from ..utils.decimal_utils import to_decimal, round_money
from .electricity_service import distribute_electricity_fee
from .electricity_calculation_service import ElectricityCalculationService
from .rent_service import (
    calculate_rent_actual_with_overrides,
    calculate_final_amount,
    is_in_probation_for_residence,
    get_active_residence_in_month,
)
from .water_meter_service import get_employee_water_fee_for_month


def precheck_settlement(
    db: Session,
    target_month: date,
) -> Dict[str, List[Dict]]:
    """
    结算前检查

    返回 {"blocking": [...], "warnings": [...]}
    """
    target_month = month_start(target_month)
    blocking = []
    warnings = []

    # 检查所有员工是否都有当月入住
    employees = db.query(Employee).filter(Employee.status == "active").all()
    rooms = db.query(Room).filter(Room.status == "active").all()

    active_room_ids = [r.id for r in rooms]

    for emp in employees:
        res = get_active_residence_in_month(db, emp.id, target_month)
        if not res:
            # 跳过没有入住的员工，不阻断
            continue

    # 检查房间电表记录
    for room in rooms:
        meter = db.query(MeterRecord).filter(
            and_(
                MeterRecord.room_id == room.id,
                MeterRecord.month == target_month,
            )
        ).first()
        if not meter:
            warnings.append({
                "type": "missing_meter",
                "message": f"{room.id}号房间（{room.room_name}）本月未录入电表",
                "ref_type": "room",
                "ref_id": room.id,
            })

    return {"blocking": blocking, "warnings": warnings}


def generate_settlement(
    db: Session,
    target_month: date,
    force: bool = False,
    use_v2: bool = True,
    water_mode: str = "double",
) -> List[MonthlySettlement]:
    """
    生成月度结算

    步骤：
    1. 获取当月有效入住员工
    2. 获取房租标准、电表读数、个人电费、个人水费
    3. 写入/更新 settlement
    
    Args:
        use_v2: 是否使用V2电表计算（总表-空调表分离架构）
        water_mode: 水费计算模式 "single"=单月 "double"=双月
    """
    target_month = month_start(target_month)

    # 已锁定月份不允许重新生成
    locked = db.query(MonthlySettlement).filter(
        and_(
            MonthlySettlement.month == target_month,
            MonthlySettlement.status == "locked",
        )
    ).first()
    if locked and not force:
        raise ValueError(f"{target_month} 月份已锁定，请先解锁")

    # 收集员工电费映射
    elec_by_emp: Dict[int, Dict] = {}
    
    if use_v2:
        # V2架构：从ElectricityCalculationService获取分摊结果
        calc_service = ElectricityCalculationService(db)
        
        # 获取所有房号总表
        main_meters = db.query(RoomMainMeterRecord).filter(
            RoomMainMeterRecord.month == target_month
        ).all()
        
        for main_meter in main_meters:
            # 计算该房号的电费分摊
            result = calc_service.calculate_room_no_electricity(
                building_id=main_meter.building_id,
                room_no=main_meter.room_no,
                month=target_month,
            )
            distributions = result['distributions']
            
            # 汇总到员工
            for dist in distributions:
                emp_id = dist['employee_id']
                if emp_id not in elec_by_emp:
                    elec_by_emp[emp_id] = {
                        "electricity_fee": Decimal("0"),
                        "ac_electricity_fee": Decimal("0")
                    }
                # V2架构中，公共电费作为普通电费，空调费单独
                elec_by_emp[emp_id]["electricity_fee"] += to_decimal(dist['common_electricity_fee'])
                elec_by_emp[emp_id]["ac_electricity_fee"] += to_decimal(dist['ac_electricity_fee'])
    else:
        # V1架构：使用旧的按套间分摊逻辑
        meter_records = db.query(MeterRecord).filter(
            MeterRecord.month == target_month
        ).all()
        
        elec_distribution: Dict[int, List] = {}
        for m in meter_records:
            elec_distribution[m.room_id] = distribute_electricity_fee(
                db, m, target_month,
            )
        
        for room_id, dists in elec_distribution.items():
            for emp_id, elec, ac in dists:
                if emp_id not in elec_by_emp:
                    elec_by_emp[emp_id] = {
                        "electricity_fee": Decimal("0"),
                        "ac_electricity_fee": Decimal("0")
                    }
                elec_by_emp[emp_id]["electricity_fee"] += to_decimal(elec)
                elec_by_emp[emp_id]["ac_electricity_fee"] += to_decimal(ac)

    # 收集所有有效入住的员工
    residences = db.query(ResidenceRecord).filter(
        ResidenceRecord.status != "invalid"
    ).all()

    settlements = []
    for res in residences:
        emp_id = res.employee_id
        # 只为当月有效入住的员工生成
        from ..utils.date_utils import stay_days_in_month
        days = stay_days_in_month(res.check_in_date, res.check_out_date, target_month)
        if days <= 0:
            continue

        room = db.query(Room).filter(Room.id == res.room_id).first()
        if not room:
            continue

        # 房租
        rent_standard = to_decimal(room.rent_standard)
        rent_actual = calculate_rent_actual_with_overrides(
            res, rent_standard, target_month,
        )

        # 个人电费
        elec = elec_by_emp.get(emp_id, {"electricity_fee": Decimal("0"), "ac_electricity_fee": Decimal("0")})
        elec_fee = round_money(elec["electricity_fee"])
        ac_fee = round_money(elec["ac_electricity_fee"])

        # 个人水费（根据模式选择）
        include_prev = (water_mode == "double")
        water_fee = get_employee_water_fee_for_month(db, emp_id, target_month)

        # 最终扣款
        total = calculate_final_amount(
            rent_actual=rent_actual,
            electricity_fee=elec_fee,
            ac_fee=ac_fee,
            water_fee=water_fee,
            deduction_minus=Decimal("0"),
            deduction_plus=Decimal("0"),
        )

        # 查询是否已存在
        existing = db.query(MonthlySettlement).filter(
            and_(
                MonthlySettlement.month == target_month,
                MonthlySettlement.employee_id == emp_id,
            )
        ).first()

        if existing:
            if existing.status == "locked":
                continue  # 跳过锁定记录
            existing.room_id = res.room_id
            existing.rent_should = rent_standard
            existing.rent_actual = rent_actual
            existing.stay_days = days
            existing.electricity_fee = elec_fee
            existing.ac_electricity_fee = ac_fee
            existing.water_fee = water_fee
            existing.total_amount = total
            existing.status = "generated"
            settlements.append(existing)
        else:
            s = MonthlySettlement(
                month=target_month,
                employee_id=emp_id,
                room_id=res.room_id,
                rent_should=rent_standard,
                rent_actual=rent_actual,
                stay_days=days,
                electricity_fee=elec_fee,
                ac_electricity_fee=ac_fee,
                water_fee=water_fee,
                deduction_minus=Decimal("0"),
                deduction_plus=Decimal("0"),
                total_amount=total,
                status="generated",
            )
            db.add(s)
            settlements.append(s)

    db.flush()
    return settlements


def lock_month(db: Session, target_month: date) -> int:
    """锁定月份"""
    target_month = month_start(target_month)
    count = db.query(MonthlySettlement).filter(
        MonthlySettlement.month == target_month
    ).update({"status": "locked"})
    db.flush()
    return count


def unlock_month(db: Session, target_month: date) -> int:
    """解锁月份"""
    target_month = month_start(target_month)
    count = db.query(MonthlySettlement).filter(
        MonthlySettlement.month == target_month
    ).update({"status": "generated"})
    db.flush()
    return count


def recalculate_settlement(
    db: Session,
    target_month: date,
    water_mode: str = "double",
) -> List[MonthlySettlement]:
    """重新计算（覆盖现有）"""
    return generate_settlement(db, target_month, force=True, water_mode=water_mode)


def calculate_realtime_settlements(
    db: Session,
    target_month: date,
    water_mode: str = "double",
) -> List[Dict]:
    """
    实时计算结算数据（不写入数据库）
    
    Args:
        target_month: 目标月份
        water_mode: 水费计算模式 "single"=单月 "double"=双月 "none"=不计算
    
    Returns:
        结算数据列表（字典格式）
    """
    target_month = month_start(target_month)
    
    # 1. 收集员工电费映射
    elec_by_emp: Dict[int, Dict] = {}
    
    # V2架构：从ElectricityCalculationService获取分摊结果
    calc_service = ElectricityCalculationService(db)
    
    # 获取所有房号总表
    main_meters = db.query(RoomMainMeterRecord).filter(
        RoomMainMeterRecord.month == target_month
    ).all()
    
    for main_meter in main_meters:
        try:
            # 计算该房号的电费分摊
            result = calc_service.calculate_room_no_electricity(
                building_id=main_meter.building_id,
                room_no=main_meter.room_no,
                month=target_month,
            )
            distributions = result['distributions']
            
            # 汇总到员工
            for dist in distributions:
                emp_id = dist['employee_id']
                if emp_id not in elec_by_emp:
                    elec_by_emp[emp_id] = {
                        "electricity_fee": Decimal("0"),
                        "ac_electricity_fee": Decimal("0")
                    }
                elec_by_emp[emp_id]["electricity_fee"] += to_decimal(dist['common_electricity_fee'])
                elec_by_emp[emp_id]["ac_electricity_fee"] += to_decimal(dist['ac_electricity_fee'])
        except Exception:
            # 如果某个房间计算失败，跳过
            continue
    
    # 2. 收集所有有效入住的员工
    residences = db.query(ResidenceRecord).filter(
        ResidenceRecord.status != "invalid"
    ).all()
    
    # 3. 计算水费（根据模式选择）
    include_prev = (water_mode == "double")
    water_by_emp = {}
    for res in residences:
        emp_id = res.employee_id
        water_by_emp[emp_id] = get_employee_water_fee_for_month(db, emp_id, target_month)
    
    # 4. 组装结算数据
    results = []
    for res in residences:
        from ..utils.date_utils import stay_days_in_month
        emp_id = res.employee_id
        
        # 只为当月有效入住的员工生成
        days = stay_days_in_month(res.check_in_date, res.check_out_date, target_month)
        if days <= 0:
            continue
        
        room = db.query(Room).filter(Room.id == res.room_id).first()
        if not room:
            continue
        
        emp = db.query(Employee).filter(Employee.id == emp_id).first()
        if not emp:
            continue
        
        building = db.query(Building).filter(Building.id == room.building_id).first()
        
        # 房租
        rent_standard = to_decimal(room.rent_standard)
        rent_actual = calculate_rent_actual_with_overrides(
            res, rent_standard, target_month,
        )
        
        # 个人电费
        elec = elec_by_emp.get(emp_id, {"electricity_fee": Decimal("0"), "ac_electricity_fee": Decimal("0")})
        elec_fee = round_money(elec["electricity_fee"])
        ac_fee = round_money(elec["ac_electricity_fee"])
        
        # 个人水费（根据水费模式）
        if water_mode == "none":
            water_fee = Decimal("0")
        else:
            water_fee = water_by_emp.get(emp_id, Decimal("0"))
        
        # 查询是否有已保存的调整数据
        existing = db.query(MonthlySettlement).filter(
            and_(
                MonthlySettlement.month == target_month,
                MonthlySettlement.employee_id == emp_id,
            )
        ).first()
        
        # 如果有已保存的调整，使用调整后的值
        if existing:
            deduction_minus = existing.deduction_minus
            deduction_plus = existing.deduction_plus
            remark = existing.remark
            status = existing.status
        else:
            deduction_minus = Decimal("0")
            deduction_plus = Decimal("0")
            remark = ""
            status = "draft"
        
        # 最终扣款
        total = calculate_final_amount(
            rent_actual=rent_actual,
            electricity_fee=elec_fee,
            ac_fee=ac_fee,
            water_fee=water_fee,
            deduction_minus=deduction_minus,
            deduction_plus=deduction_plus,
        )
        
        results.append({
            "id": existing.id if existing else 0,
            "month": target_month,
            "employee_id": emp_id,
            "employee_no": emp.employee_no,
            "employee_name": emp.name,
            "company": emp.company,
            "department": emp.department,
            "position": emp.position,
            "room_id": res.room_id,
            "room_no": room.room_no,
            "room_name": room.room_name,
            "building_id": room.building_id,
            "building_no": building.building_no if building else "",
            "rent_should": float(rent_standard),
            "rent_actual": float(rent_actual),
            "stay_days": days,
            "electricity_fee": float(elec_fee),
            "ac_electricity_fee": float(ac_fee),
            "water_fee": float(water_fee),
            "deduction_minus": float(deduction_minus),
            "deduction_plus": float(deduction_plus),
            "total_amount": float(total),
            "remark": remark,
            "status": status,
        })
    
    return results


__all__ = [
    "precheck_settlement",
    "generate_settlement",
    "lock_month",
    "unlock_month",
    "recalculate_settlement",
    "calculate_realtime_settlements",
]
