"""电费服务：普通电费 + 空调电费 + 分摊 + 尾差处理"""
from decimal import Decimal
from datetime import date
from typing import List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_

from ..models import MeterRecord, ResidenceRecord
from ..utils.date_utils import month_start, stay_days_in_month
from ..utils.decimal_utils import (
    to_decimal, round_money, round_degree, allocate_with_remainder,
)


def calculate_room_total_fee(meter: MeterRecord) -> Decimal:
    """计算房间普通电费"""
    degree = to_decimal(meter.total_degree)
    price = to_decimal(meter.electricity_price)
    return round_money(degree * price)


def calculate_room_ac_fee(meter: MeterRecord) -> Decimal:
    """计算房间空调电费"""
    degree = to_decimal(meter.ac_degree)
    price = to_decimal(meter.ac_unit_price)
    return round_money(degree * price)


def is_residence_valid_for_electricity(
    res: ResidenceRecord,
    target_month: date,
) -> bool:
    """
    判断入住记录是否参与电费分摊

    规则：
    - 状态有效
    - 入住期内（在月中属于有效入住人员）
    - 非出差/休假
    """
    if res.status in ("invalid", "business_trip", "leave"):
        return False

    days = stay_days_in_month(res.check_in_date, res.check_out_date, target_month)
    return days > 0


def get_valid_occupants_for_room(
    db: Session,
    room_id: int,
    target_month: date,
) -> List[ResidenceRecord]:
    """获取房间当月有效入住人员（用于电费分摊）"""
    target_month = month_start(target_month)
    records = db.query(ResidenceRecord).filter(
        and_(
            ResidenceRecord.room_id == room_id,
            ResidenceRecord.status != "invalid",
        )
    ).all()
    return [r for r in records if is_residence_valid_for_electricity(r, target_month)]


def distribute_electricity_fee(
    db: Session,
    meter: MeterRecord,
    target_month: date,
) -> List[Tuple[int, Decimal, Decimal]]:
    """
    分摊电费（普通 + 空调）给房间所有有效入住人员

    返回 [(employee_id, personal_electricity_fee, personal_ac_fee), ...]

    规则：
    - 夫妻间：只有主要缴费人承担全部水电费
    - 出差：电费=0
    - 处理尾差（最后一人承担）
    """
    target_month = month_start(target_month)
    occupants = get_valid_occupants_for_room(db, meter.room_id, target_month)

    total_fee = to_decimal(meter.total_fee)
    ac_fee = to_decimal(meter.ac_fee)

    if not occupants:
        return []

    # 区分主要缴费人与其他人员
    primary = [r for r in occupants if r.is_primary_payer == 1]
    others = [r for r in occupants if r.is_primary_payer != 1]

    # 如果有主要缴费人（夫妻间），他承担全部
    if primary:
        # 主要缴费人承担全部
        results = []
        results.append((
            primary[0].employee_id,
            round_money(total_fee),
            round_money(ac_fee),
        ))
        # 其他人不分摊水电费（但房租仍正常）
        for r in others:
            results.append((r.employee_id, Decimal("0.00"), Decimal("0.00")))
        return results

    # 普通情况：所有人平均分摊，处理尾差
    n = len(occupants)
    elec_alloc = allocate_with_remainder(total_fee, n)
    ac_alloc = allocate_with_remainder(ac_fee, n)

    # 出差人员水电费=0
    results = []
    for i, r in enumerate(occupants):
        if r.status == "business_trip":
            results.append((r.employee_id, Decimal("0.00"), Decimal("0.00")))
        else:
            results.append((r.employee_id, elec_alloc[i], ac_alloc[i]))

    return results


def calculate_all_electricity_for_month(
    db: Session,
    target_month: date,
    ac_unit_price: Decimal | None = None,
) -> int:
    """
    计算某月所有房间的电费

    返回计算的房间数
    """
    target_month = month_start(target_month)
    records = db.query(MeterRecord).filter(MeterRecord.month == target_month).all()
    count = 0
    for m in records:
        # 计算用电量
        prev = to_decimal(m.previous_reading)
        curr = to_decimal(m.current_reading)
        if curr >= prev and curr > 0:
            m.total_degree = round_degree(curr - prev)
            m.total_fee = round_money(m.total_degree * to_decimal(m.electricity_price))

        prev_ac = to_decimal(m.ac_previous_reading)
        curr_ac = to_decimal(m.ac_current_reading)
        if curr_ac >= prev_ac and curr_ac > 0:
            m.ac_degree = round_degree(curr_ac - prev_ac)
            if ac_unit_price is not None and ac_unit_price > 0:
                m.ac_unit_price = ac_unit_price
            if to_decimal(m.ac_unit_price) > 0:
                m.ac_fee = round_money(m.ac_degree * to_decimal(m.ac_unit_price))

        count += 1
    db.flush()
    return count


__all__ = [
    "calculate_room_total_fee",
    "calculate_room_ac_fee",
    "is_residence_valid_for_electricity",
    "get_valid_occupants_for_room",
    "distribute_electricity_fee",
    "calculate_all_electricity_for_month",
]
