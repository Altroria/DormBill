"""结算服务：生成月度最终扣款"""
from decimal import Decimal
from datetime import date
from typing import List, Dict
from sqlalchemy.orm import Session
from sqlalchemy import and_

from ..models import (
    MonthlySettlement, MeterRecord, ResidenceRecord, Room, Employee,
)
from ..utils.date_utils import month_start, month_end
from ..utils.decimal_utils import to_decimal, round_money
from .electricity_service import distribute_electricity_fee
from .rent_service import (
    calculate_rent_actual_with_overrides,
    calculate_final_amount,
    is_in_probation_for_residence,
    get_active_residence_in_month,
)
from .water_service import get_employee_water_fee_for_month


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
) -> List[MonthlySettlement]:
    """
    生成月度结算

    步骤：
    1. 获取当月有效入住员工
    2. 获取房租标准、电表读数、个人电费、个人水费
    3. 写入/更新 settlement
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

    # 获取当月所有电表记录（用于按房间查找员工电费）
    meter_records = db.query(MeterRecord).filter(
        MeterRecord.month == target_month
    ).all()
    meter_by_room = {m.room_id: m for m in meter_records}

    # 计算每个房间的电费分摊
    elec_distribution: Dict[int, List] = {}  # room_id -> [(employee_id, elec, ac)]
    for m in meter_records:
        elec_distribution[m.room_id] = distribute_electricity_fee(
            db, m, target_month,
        )

    # 收集员工电费映射
    elec_by_emp: Dict[int, Dict] = {}
    for room_id, dists in elec_distribution.items():
        for emp_id, elec, ac in dists:
            if emp_id not in elec_by_emp:
                elec_by_emp[emp_id] = {"electricity_fee": Decimal("0"), "ac_electricity_fee": Decimal("0")}
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

        # 个人水费
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
) -> List[MonthlySettlement]:
    """重新计算（覆盖现有）"""
    return generate_settlement(db, target_month, force=True)


__all__ = [
    "precheck_settlement",
    "generate_settlement",
    "lock_month",
    "unlock_month",
    "recalculate_settlement",
]
