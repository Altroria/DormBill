"""后端核心计算测试"""
import pytest
from decimal import Decimal
from datetime import date

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.utils.decimal_utils import (
    round_money, allocate_with_remainder, to_decimal,
)
from app.utils.date_utils import (
    days_in_month, stay_days_in_month, add_months,
    is_in_probation, half_month_rule_valid, month_start, month_end,
)


class TestDecimalUtils:
    """金额计算测试"""

    def test_allocate_remainder_even(self):
        """能整除的情况"""
        result = allocate_with_remainder(Decimal("100.00"), 4)
        assert len(result) == 4
        assert all(isinstance(r, Decimal) for r in result)
        assert sum(result) == Decimal("100.00")

    def test_allocate_remainder_three(self):
        """电费尾差测试：100÷3"""
        result = allocate_with_remainder(Decimal("100.00"), 3)
        assert result == [Decimal("33.33"), Decimal("33.33"), Decimal("33.34")]
        assert sum(result) == Decimal("100.00")

    def test_allocate_remainder_six(self):
        """水费尾差测试：100÷6"""
        result = allocate_with_remainder(Decimal("100.00"), 6)
        # 每人 16.666... → 5人16.67，1人16.65
        assert len(result) == 6
        assert result[0] == result[1] == result[2] == result[3] == result[4]
        assert result[5] < result[0]
        assert sum(result) == Decimal("100.00")

    def test_allocate_zero(self):
        """总额为0"""
        result = allocate_with_remainder(Decimal("0"), 3)
        assert result == [Decimal("0.00"), Decimal("0.00"), Decimal("0.00")]

    def test_allocate_n_zero(self):
        """人数为0"""
        result = allocate_with_remainder(Decimal("100"), 0)
        assert result == []

    def test_round_money(self):
        """金额四舍五入"""
        assert round_money("168.565") == Decimal("168.57")
        assert round_money("168.564") == Decimal("168.56")
        assert round_money(100) == Decimal("100.00")

    def test_electricity_fee_calc(self):
        """电费计算：344 × 0.49"""
        degree = Decimal("344")
        price = Decimal("0.49")
        fee = round_money(degree * price)
        assert fee == Decimal("168.56")


class TestDateUtils:
    """日期计算测试"""

    def test_days_in_month(self):
        """当月天数"""
        assert days_in_month(date(2026, 7, 15)) == 31
        assert days_in_month(date(2026, 2, 1)) == 28
        assert days_in_month(date(2024, 2, 1)) == 29  # 闰年

    def test_stay_days_full_month(self):
        """整月入住：7月1日~31日"""
        check_in = date(2026, 7, 1)
        check_out = date(2026, 7, 31)
        days = stay_days_in_month(check_in, check_out, date(2026, 7, 15))
        assert days == 31

    def test_stay_days_partial_start(self):
        """月中入住：7月10日入住"""
        check_in = date(2026, 7, 10)
        check_out = None
        days = stay_days_in_month(check_in, check_out, date(2026, 7, 15))
        assert days == 22  # 7/10~7/31 = 22天

    def test_stay_days_partial_end(self):
        """月中搬离：7月7日离宿"""
        check_in = date(2026, 7, 1)
        check_out = date(2026, 7, 7)
        days = stay_days_in_month(check_in, check_out, date(2026, 7, 15))
        assert days == 7  # 7/1~7/7 = 7天

    def test_stay_days_move_out_middle(self):
        """月中换房：7月24日换房（搬离日不计房租 → exclusive）"""
        check_in = date(2026, 7, 1)
        check_out = date(2026, 7, 24)
        # 换房时搬离日不计房租，用 exclusive 模式
        days = stay_days_in_month(check_in, check_out, date(2026, 7, 15), check_out_exclusive=True)
        assert days == 23  # 7/1~7/23 = 23天（搬离日不计）

    def test_stay_days_not_yet(self):
        """尚未入住"""
        check_in = date(2026, 8, 1)
        check_out = None
        days = stay_days_in_month(check_in, check_out, date(2026, 7, 15))
        assert days == 0

    def test_stay_days_already_left(self):
        """已搬离（早于月初）"""
        check_in = date(2026, 6, 1)
        check_out = date(2026, 6, 30)
        days = stay_days_in_month(check_in, check_out, date(2026, 7, 15))
        assert days == 0

    def test_probation_three_months(self):
        """试用期3个月：7月1日入住"""
        check_in = date(2026, 7, 1)
        # 7月：试用期
        assert is_in_probation(check_in, 3, date(2026, 7, 15)) is True
        # 8月：试用期
        assert is_in_probation(check_in, 3, date(2026, 8, 1)) is True
        # 9月：试用期
        assert is_in_probation(check_in, 3, date(2026, 9, 1)) is True
        # 10月：试用期结束
        assert is_in_probation(check_in, 3, date(2026, 10, 1)) is False

    def test_probation_zero(self):
        """无试用期"""
        check_in = date(2026, 7, 1)
        assert is_in_probation(check_in, 0, date(2026, 7, 15)) is False

    def test_half_month_rule(self):
        """半月规则测试"""
        # 住22天 > 15天 → 有效
        check_in = date(2026, 7, 10)
        check_out = None
        assert half_month_rule_valid(check_in, check_out, date(2026, 7, 15)) is True

        # 住10天 ≤ 15天 → 无效
        check_in = date(2026, 7, 22)
        check_out = None
        assert half_month_rule_valid(check_in, check_out, date(2026, 7, 15)) is False

    def test_add_months(self):
        """加月数"""
        assert add_months(date(2026, 7, 1), 3) == date(2026, 10, 1)
        assert add_months(date(2026, 12, 15), 1) == date(2027, 1, 15)
        assert add_months(date(2026, 1, 31), 1) == date(2026, 2, 28)  # 非闰年


class TestRentCalculation:
    """房租计算测试"""

    def test_rent_full_month(self):
        """整月入住房租折算"""
        from app.services.rent_service import calculate_rent_actual
        rent_standard = Decimal("500")
        check_in = date(2026, 7, 1)
        check_out = None
        result = calculate_rent_actual(rent_standard, check_in, check_out, 0, date(2026, 7, 15))
        assert result == Decimal("500.00")

    def test_rent_partial_month_7days(self):
        """月中离宿房租折算：7天"""
        from app.services.rent_service import calculate_rent_actual
        rent_standard = Decimal("500")
        check_in = date(2026, 7, 1)
        check_out = date(2026, 7, 7)
        result = calculate_rent_actual(rent_standard, check_in, check_out, 0, date(2026, 7, 15))
        assert result == Decimal("112.90")  # 500 * 7/31 ≈ 112.90

    def test_rent_partial_month_24days(self):
        """月中入住房租折算：24天"""
        from app.services.rent_service import calculate_rent_actual
        rent_standard = Decimal("500")
        check_in = date(2026, 7, 8)
        check_out = None
        result = calculate_rent_actual(rent_standard, check_in, check_out, 0, date(2026, 7, 15))
        assert result == Decimal("387.10")  # 500 * 24/31 ≈ 387.10

    def test_rent_probation_free(self):
        """试用期免租"""
        from app.services.rent_service import calculate_rent_actual
        rent_standard = Decimal("500")
        check_in = date(2026, 7, 1)
        check_out = None
        # 试用期3个月，7月在试用期内
        result = calculate_rent_actual(rent_standard, check_in, check_out, 3, date(2026, 7, 15))
        assert result == Decimal("0.00")

    def test_rent_probation_ended(self):
        """试用期结束"""
        from app.services.rent_service import calculate_rent_actual
        rent_standard = Decimal("500")
        check_in = date(2026, 7, 1)
        check_out = None
        # 试用期3个月，10月已结束
        result = calculate_rent_actual(rent_standard, check_in, check_out, 3, date(2026, 10, 1))
        assert result == Decimal("500.00")


class TestElectricityDistribution:
    """电费分摊测试"""

    def test_distribute_two_persons(self):
        """双人房间电费分摊：50.96 ÷ 2"""
        result = allocate_with_remainder(Decimal("50.96"), 2)
        assert result == [Decimal("25.48"), Decimal("25.48")]
        assert sum(result) == Decimal("50.96")

    def test_distribute_three_persons(self):
        """三人房间电费分摊：100 ÷ 3（尾差）"""
        result = allocate_with_remainder(Decimal("100.00"), 3)
        assert result == [Decimal("33.33"), Decimal("33.33"), Decimal("33.34")]
        assert sum(result) == Decimal("100.00")

    def test_ac_fee_calc(self):
        """空调电费计算：24度 × 0.49"""
        degree = Decimal("24")
        price = Decimal("0.49")
        fee = round_money(degree * price)
        assert fee == Decimal("11.76")


class TestWaterDistribution:
    """水费分摊测试"""

    def test_water_distribute_six_persons(self):
        """6人水费分摊：100 ÷ 6"""
        result = allocate_with_remainder(Decimal("100.00"), 6)
        assert len(result) == 6
        # 5人16.67，1人16.65
        assert result[0] == result[1] == result[2] == result[3] == result[4] == Decimal("16.67")
        assert result[5] == Decimal("16.65")
        assert sum(result) == Decimal("100.00")

    def test_water_distribute_three(self):
        """3人水费分摊：100 ÷ 3（尾差）"""
        result = allocate_with_remainder(Decimal("100.00"), 3)
        assert result == [Decimal("33.33"), Decimal("33.33"), Decimal("33.34")]
        assert sum(result) == Decimal("100.00")


class TestFinalAmount:
    """最终扣款测试"""

    def test_final_amount_formula(self):
        """最终扣款公式"""
        from app.services.rent_service import calculate_final_amount
        result = calculate_final_amount(
            rent_actual=Decimal("700"),
            electricity_fee=Decimal("25.48"),
            ac_fee=Decimal("25.48"),
            water_fee=Decimal("16.67"),
            deduction_minus=Decimal("10"),
            deduction_plus=Decimal("20"),
        )
        # 700 + 25.48 + 25.48 + 16.67 - 10 + 20 = 777.63
        assert result == Decimal("777.63")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
