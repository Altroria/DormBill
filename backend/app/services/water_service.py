"""水费服务：半月规则 + 分摊 + 尾差"""
from decimal import Decimal
from datetime import date
from typing import List, Dict, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_

from ..models import (
    WaterExpense, WaterAllocation, ResidenceRecord, Room,
)
from ..utils.date_utils import (
    month_start, month_end, stay_days_in_month, half_month_rule_valid,
    add_months,
)
from ..utils.decimal_utils import to_decimal, round_money, allocate_with_remainder


def get_valid_residents_for_water_period(
    db: Session,
    building_id: int,
    period_start: date,
    period_end: date,
) -> List[Dict]:
    """
    获取某楼栋在某水费周期内的有效入住人员

    返回 [{"residence": ..., "room": ..., "month1_days": int, "month2_days": int, "is_valid": bool}]
    """
    month1 = month_start(period_start)
    month2 = month_start(add_months(period_start, 1))

    # 该楼栋所有房间
    rooms = db.query(Room).filter(
        and_(Room.building_id == building_id, Room.status == "active")
    ).all()
    room_ids = [r.id for r in rooms]
    if not room_ids:
        return []

    # 入住记录
    records = db.query(ResidenceRecord).filter(
        and_(
            ResidenceRecord.room_id.in_(room_ids),
            ResidenceRecord.status != "invalid",
        )
    ).all()

    results = []
    for r in records:
        days1 = stay_days_in_month(r.check_in_date, r.check_out_date, month1)
        days2 = stay_days_in_month(r.check_in_date, r.check_out_date, month2)

        # 半月规则：每月天数 > 15 即视为有效
        valid1 = days1 > 15
        valid2 = days2 > 15
        is_valid = valid1 or valid2  # 任一月有效即参与分摊

        # 排除出差（备注含"出差"）
        if r.remark and "出差" in r.remark:
            is_valid = False

        # 排除夫妻间非主缴费人
        if r.is_primary_payer != 1 and r.remark and "夫妻间" in r.remark:
            is_valid = False

        results.append({
            "residence": r,
            "room_id": r.room_id,
            "month1_days": days1,
            "month2_days": days2,
            "is_valid": is_valid,
        })

    return results


def allocate_water_expense(
    db: Session,
    water_expense: WaterExpense,
) -> List[WaterAllocation]:
    """
    生成水费分摊

    步骤：
    1. 获取有效入住人员（半月规则）
    2. 总数 = 楼栋水费
    3. 每人水费 = 总数 ÷ 人数
    4. 处理尾差
    """
    residents = get_valid_residents_for_water_period(
        db, water_expense.building_id,
        water_expense.period_start, water_expense.period_end,
    )
    valid_residents = [r for r in residents if r["is_valid"]]
    total_amount = to_decimal(water_expense.total_amount)

    # 清除已有分摊
    db.query(WaterAllocation).filter(
        WaterAllocation.water_expense_id == water_expense.id
    ).delete()

    allocations = []
    if not valid_residents:
        water_expense.status = "allocated"
        db.flush()
        return allocations

    n = len(valid_residents)
    amounts = allocate_with_remainder(total_amount, n)

    for i, r in enumerate(valid_residents):
        alloc = WaterAllocation(
            water_expense_id=water_expense.id,
            employee_id=r["residence"].employee_id,
            room_id=r["room_id"],
            amount=amounts[i],
            month1_days=r["month1_days"],
            month2_days=r["month2_days"],
            is_valid=1,
        )
        db.add(alloc)
        allocations.append(alloc)

    water_expense.status = "allocated"
    db.flush()
    return allocations


def update_water_allocation_amount(
    db: Session,
    allocation_id: int,
    new_amount: Decimal,
    remark: str | None = None,
) -> WaterAllocation:
    """更新单条分摊金额"""
    alloc = db.query(WaterAllocation).filter(WaterAllocation.id == allocation_id).first()
    if not alloc:
        raise ValueError(f"分摊记录不存在: {allocation_id}")
    alloc.amount = round_money(new_amount)
    if remark is not None:
        alloc.remark = remark
    db.flush()
    return alloc


def rebalance_water_allocations(
    db: Session,
    water_expense_id: int,
    manual_adjustments: Dict[int, Decimal],
) -> List[WaterAllocation]:
    """
    重新平衡水费分摊

    保持总额不变，手动调整的部分由其他未调整的人均分剩余
    """
    allocs = db.query(WaterAllocation).filter(
        WaterAllocation.water_expense_id == water_expense_id
    ).all()
    if not allocs:
        return []

    expense = db.query(WaterExpense).filter(WaterExpense.id == water_expense_id).first()
    if not expense:
        return []

    total = to_decimal(expense.total_amount)
    manual_total = sum((to_decimal(v) for v in manual_adjustments.values()), Decimal("0"))
    remaining = total - manual_total

    # 未手动调整的人
    remaining_count = len(allocs) - len(manual_adjustments)
    if remaining_count <= 0:
        return allocs

    per_person = remaining / remaining_count

    for alloc in allocs:
        if alloc.id in manual_adjustments:
            alloc.amount = round_money(manual_adjustments[alloc.id])
            alloc.remark = alloc.remark or "人工调整"

    db.flush()
    return allocs


def get_employee_water_fee_for_month(
    db: Session,
    employee_id: int,
    target_month: date,
) -> Decimal:
    """
    获取员工在指定月份应承担的水费

    - 查找覆盖该月的水费周期
    - 返回该员工在该周期内的分摊金额
    """
    month1 = month_start(target_month)
    month2 = month_end(target_month)

    expenses = db.query(WaterExpense).filter(
        and_(
            WaterExpense.status.in_(["allocated", "settled"]),
            WaterExpense.period_start <= month2,
            WaterExpense.period_end >= month1,
        )
    ).all()

    total = Decimal("0")
    for exp in expenses:
        alloc = db.query(WaterAllocation).filter(
            and_(
                WaterAllocation.water_expense_id == exp.id,
                WaterAllocation.employee_id == employee_id,
            )
        ).first()
        if alloc:
            total += to_decimal(alloc.amount)
    return round_money(total)


__all__ = [
    "get_valid_residents_for_water_period",
    "allocate_water_expense",
    "update_water_allocation_amount",
    "rebalance_water_allocations",
    "get_employee_water_fee_for_month",
]
