"""房租服务：按天数折算、试用期免租、换房计算"""
from decimal import Decimal
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import and_

from ..models import ResidenceRecord
from ..utils.date_utils import (
    month_start, month_end, days_in_month, stay_days_in_month,
    is_in_probation,
)
from ..utils.decimal_utils import to_decimal, round_money


def calculate_rent_should(
    rent_standard: Decimal,
    target_month: date,
) -> Decimal:
    """
    应住房租 = 房租标准（不考虑入住天数，仅做基础）
    """
    return to_decimal(rent_standard)


def calculate_stay_days(
    check_in: date,
    check_out: date | None,
    target_month: date,
) -> int:
    """计算当月实际入住天数"""
    return stay_days_in_month(check_in, check_out, target_month)


def is_in_probation_for_residence(
    res: ResidenceRecord,
    target_month: date,
) -> bool:
    """判断入住记录在指定月份是否处于试用期"""
    return is_in_probation(res.check_in_date, res.probation_months, target_month)


def calculate_rent_actual(
    rent_standard: Decimal,
    check_in: date,
    check_out: date | None,
    probation_months: int,
    target_month: date,
) -> Decimal:
    """
    计算实扣房租

    公式：rent_standard × 入住天数 ÷ 当月总天数
    试用期 → 实扣 = 0
    """
    # 试用期判断
    if is_in_probation(check_in, probation_months, target_month):
        return Decimal("0.00")

    days = stay_days_in_month(check_in, check_out, target_month)
    total_days = days_in_month(target_month)
    if total_days == 0:
        return Decimal("0.00")

    prorate = Decimal(days) / Decimal(total_days)
    return round_money(to_decimal(rent_standard) * prorate)


def calculate_rent_actual_with_overrides(
    res: ResidenceRecord,
    rent_standard: Decimal,
    target_month: date,
    override_actual: Decimal | None = None,
) -> Decimal:
    """
    计算实扣房租（支持覆盖值）
    """
    if override_actual is not None:
        return to_decimal(override_actual)
    return calculate_rent_actual(
        rent_standard,
        res.check_in_date,
        res.check_out_date,
        res.probation_months,
        target_month,
    )


def get_active_residence_in_month(
    db: Session,
    employee_id: int,
    target_month: date,
) -> ResidenceRecord | None:
    """
    获取员工在指定月份的有效入住记录

    入住期跨越目标月份中任意一天即视为有效
    """
    target_month = month_start(target_month)
    target_end = month_end(target_month)
    records = db.query(ResidenceRecord).filter(
        and_(
            ResidenceRecord.employee_id == employee_id,
            ResidenceRecord.status != "invalid",
        )
    ).all()
    for r in records:
        days = stay_days_in_month(r.check_in_date, r.check_out_date, target_month)
        if days > 0:
            return r
    return None


def calculate_final_amount(
    rent_actual: Decimal,
    electricity_fee: Decimal,
    ac_fee: Decimal,
    water_fee: Decimal,
    deduction_minus: Decimal,
    deduction_plus: Decimal,
) -> Decimal:
    """
    最终扣款 = 实扣房租 + 个人电费 + 个人空调电费 + 个人水费 - 补扣- + 补扣+
    """
    total = (
        to_decimal(rent_actual)
        + to_decimal(electricity_fee)
        + to_decimal(ac_fee)
        + to_decimal(water_fee)
        - to_decimal(deduction_minus)
        + to_decimal(deduction_plus)
    )
    return round_money(total)


__all__ = [
    "calculate_rent_should",
    "calculate_stay_days",
    "is_in_probation_for_residence",
    "calculate_rent_actual",
    "calculate_rent_actual_with_overrides",
    "get_active_residence_in_month",
    "calculate_final_amount",
]
