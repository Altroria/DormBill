"""Decimal 金额计算工具"""
from decimal import Decimal, ROUND_HALF_UP
from typing import List


# 金额精度：两位小数
MONEY_QUANTIZE = Decimal("0.01")
# 度数精度：两位小数
DEGREE_QUANTIZE = Decimal("0.01")


def to_decimal(value, default: Decimal = Decimal("0")) -> Decimal:
    """转换为 Decimal"""
    if value is None or value == "":
        return default
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def round_money(value) -> Decimal:
    """金额四舍五入到两位小数（ROUND_HALF_UP）"""
    return to_decimal(value).quantize(MONEY_QUANTIZE, rounding=ROUND_HALF_UP)


def round_degree(value) -> Decimal:
    """度数四舍五入到两位小数"""
    return to_decimal(value).quantize(DEGREE_QUANTIZE, rounding=ROUND_HALF_UP)


def allocate_with_remainder(total: Decimal, n: int) -> List[Decimal]:
    """
    均分金额到 n 份，处理尾差（最后一人承担尾差）

    例如 total=100, n=3 → [33.33, 33.33, 33.34]
    保证 sum(allocated) == round_money(total)
    """
    if n <= 0:
        return []
    total = round_money(total)
    if total == 0:
        return [Decimal("0.00")] * n

    # 单人份额 = 总额 / 人数
    per_share = total / n
    per_rounded = round_money(per_share)

    # 基础分配
    allocations = [per_rounded] * n
    # 计算尾差
    diff = total - sum(allocations)
    if diff != 0:
        # 尾差分配到最后一人
        allocations[-1] = round_money(per_rounded + diff)

    return allocations


def safe_sum(values) -> Decimal:
    """安全累加 Decimal"""
    return sum((to_decimal(v) for v in values), Decimal("0"))


__all__ = [
    "MONEY_QUANTIZE",
    "DEGREE_QUANTIZE",
    "to_decimal",
    "round_money",
    "round_degree",
    "allocate_with_remainder",
    "safe_sum",
]
