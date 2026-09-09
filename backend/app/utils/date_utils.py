"""日期计算工具"""
from datetime import date, timedelta
from calendar import monthrange


def parse_date(value) -> date:
    """解析日期字符串"""
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        value = value.strip().replace("/", "-")
        if len(value) == 7:  # 2026-07
            return date.fromisoformat(value + "-01")
        return date.fromisoformat(value)
    raise ValueError(f"无法解析日期: {value}")


def month_start(d: date) -> date:
    """月份第一天"""
    return d.replace(day=1)


def month_end(d: date) -> date:
    """月份最后一天"""
    _, last_day = monthrange(d.year, d.month)
    return d.replace(day=last_day)


def days_in_month(d: date) -> int:
    """当月总天数"""
    _, last_day = monthrange(d.year, d.month)
    return last_day


def stay_days_in_month(
    check_in: date,
    check_out: date | None,
    target_month: date,
    check_out_exclusive: bool = False,
) -> int:
    """
    计算员工在 target_month 月的有效入住天数

    公式：min(搬离日, 月末) - max(入住日, 月初) + 1
    对于换房场景（搬离日不计房租），设 check_out_exclusive=True：
    公式：min(搬离日-1, 月末) - max(入住日, 月初) + 1
    """
    if not check_in:
        return 0

    month_first = month_start(target_month)
    month_last = month_end(target_month)

    # 员工搬离日早于月初 → 整月未入住
    if check_out and check_out <= month_first:
        return 0
    # 员工入住日晚于月末 → 整月未入住
    if check_in > month_last:
        return 0

    effective_start = max(check_in, month_first)
    if check_out_exclusive and check_out:
        effective_end = min(check_out - timedelta(days=1), month_last)
    else:
        effective_end = check_out if check_out else month_last
    effective_end = min(effective_end, month_last)

    days = (effective_end - effective_start).days + 1
    return max(0, days)


def add_months(d: date, months: int) -> date:
    """日期加月数"""
    month = d.month - 1 + months
    year = d.year + month // 12
    month = month % 12 + 1
    day = min(d.day, monthrange(year, month)[1])
    return date(year, month, day)


def is_in_probation(
    check_in: date,
    probation_months: int,
    target_month: date,
) -> bool:
    """
    判断员工在 target_month 月是否处于试用期

    试用期 = [入住日, 入住日 + N个月)
    """
    if probation_months <= 0:
        return False
    probation_end = add_months(check_in, probation_months)
    # 月份任意一天处于试用期即视为试用期
    return month_start(target_month) < probation_end


def half_month_rule_valid(
    check_in: date,
    check_out: date | None,
    target_month: date,
    threshold: int = 15,
) -> bool:
    """
    半月规则：该月在 target_month 月有效天数 > threshold 视为有效
    """
    days = stay_days_in_month(check_in, check_out, target_month)
    return days > threshold


def format_month(d: date) -> str:
    """格式化为 YYYY-MM"""
    return f"{d.year:04d}-{d.month:02d}"


__all__ = [
    "parse_date",
    "month_start",
    "month_end",
    "days_in_month",
    "stay_days_in_month",
    "add_months",
    "is_in_probation",
    "half_month_rule_valid",
    "format_month",
]
