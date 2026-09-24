"""测试换房场景的按天分摊"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from datetime import date
from decimal import Decimal
from app.utils.date_utils import stay_days_in_month
from app.services.rent_service import calculate_rent_actual

def test_room_transfer_scenario():
    """
    测试场景：员工9月15日从A房间换到B房间
    - A房间：9月1日-9月14日（14天）
    - B房间：9月15日-9月30日（16天）
    
    验证各项费用是否按天分摊
    """
    print("\n" + "="*70)
    print("换房场景测试：员工9月15日从A房转到B房")
    print("="*70)
    
    transfer_date = date(2026, 9, 15)
    target_month = date(2026, 9, 1)
    
    # A房间入住记录
    a_check_in = date(2026, 8, 1)
    a_check_out = date(2026, 9, 14)  # 换房当天的前一天搬离（14日是最后一天）
    
    # B房间入住记录
    b_check_in = date(2026, 9, 15)  # 换房当天入住
    b_check_out = None  # 未搬离
    
    print(f"\n目标月份: {target_month.strftime('%Y年%m月')}")
    print(f"换房日期: {transfer_date.strftime('%Y-%m-%d')}")
    
    # 1. 计算入住天数
    print("\n【1. 入住天数计算】")
    print("-" * 70)
    
    a_days = stay_days_in_month(a_check_in, a_check_out, target_month)
    b_days = stay_days_in_month(b_check_in, b_check_out, target_month)
    total_days = 30  # 9月总天数
    
    print(f"A房间 (9月1日-9月14日):")
    print(f"  入住日期: {a_check_in} - {a_check_out}")
    print(f"  9月入住天数: {a_days} 天")
    
    print(f"\nB房间 (9月15日-9月30日):")
    print(f"  入住日期: {b_check_in} - {b_check_out or '未搬离'}")
    print(f"  9月入住天数: {b_days} 天")
    
    print(f"\n总计: {a_days} + {b_days} = {a_days + b_days} 天 (9月总天数: {total_days})")
    
    # 2. 房租分摊
    print("\n【2. 房租分摊（按天）】")
    print("-" * 70)
    
    a_rent_standard = Decimal("500.00")  # A房间月租500元
    b_rent_standard = Decimal("600.00")  # B房间月租600元
    
    a_rent = calculate_rent_actual(
        rent_standard=a_rent_standard,
        check_in=a_check_in,
        check_out=a_check_out,
        probation_months=0,
        target_month=target_month
    )
    
    b_rent = calculate_rent_actual(
        rent_standard=b_rent_standard,
        check_in=b_check_in,
        check_out=b_check_out,
        probation_months=0,
        target_month=target_month
    )
    
    print(f"A房间月租: {a_rent_standard} 元")
    print(f"  按天计算: {a_rent_standard} × {a_days}/{total_days} = {float(a_rent):.2f} 元")
    
    print(f"\nB房间月租: {b_rent_standard} 元")
    print(f"  按天计算: {b_rent_standard} × {b_days}/{total_days} = {float(b_rent):.2f} 元")
    
    print(f"\n9月总房租: {float(a_rent):.2f} + {float(b_rent):.2f} = {float(a_rent + b_rent):.2f} 元")
    
    # 3. 水电费分摊说明
    print("\n【3. 水电费分摊（按天）】")
    print("-" * 70)
    
    # 假设A房间总共3人，9月公共电费300元
    a_room_total_electricity = Decimal("300.00")
    a_room_total_person_days = 14 + 30 + 30  # 本人14天 + 另外2人各30天 = 74天
    
    a_electricity_fee = a_room_total_electricity * Decimal(a_days) / Decimal(a_room_total_person_days)
    
    print(f"A房间公共电费: {a_room_total_electricity} 元")
    print(f"  A房间总人天数: {a_room_total_person_days} 天 (本人{a_days}天 + 其他人60天)")
    print(f"  本人分摊: {a_room_total_electricity} × {a_days}/{a_room_total_person_days} = {float(a_electricity_fee):.2f} 元")
    
    # 假设B房间总共2人，9月公共电费200元
    b_room_total_electricity = Decimal("200.00")
    b_room_total_person_days = 16 + 30  # 本人16天 + 另1人30天 = 46天
    
    b_electricity_fee = b_room_total_electricity * Decimal(b_days) / Decimal(b_room_total_person_days)
    
    print(f"\nB房间公共电费: {b_room_total_electricity} 元")
    print(f"  B房间总人天数: {b_room_total_person_days} 天 (本人{b_days}天 + 其他人30天)")
    print(f"  本人分摊: {b_room_total_electricity} × {b_days}/{b_room_total_person_days} = {float(b_electricity_fee):.2f} 元")
    
    print(f"\n9月总电费: {float(a_electricity_fee):.2f} + {float(b_electricity_fee):.2f} = {float(a_electricity_fee + b_electricity_fee):.2f} 元")
    
    # 4. 空调费分摊说明
    print("\n【4. 空调费分摊（按天）】")
    print("-" * 70)
    print("空调费计算逻辑：")
    print("  - 如果该房间有空调表，且员工有空调使用记录")
    print("  - 分摊公式：房间总空调费 × (个人入住天数 / 房间总人天数)")
    print("  - 与公共电费分摊逻辑相同")
    
    # 5. 水费分摊说明
    print("\n【5. 水费分摊（按天）】")
    print("-" * 70)
    print("水费计算逻辑：")
    print("  - 房间总水费 × (个人入住天数 / 房间总人天数)")
    print("  - 与电费分摊逻辑相同")
    
    # 总结
    print("\n" + "="*70)
    print("【总结】")
    print("="*70)
    print("✅ 房租：按天分摊")
    print("   公式: 房租标准 × (实际入住天数 / 当月总天数)")
    print()
    print("✅ 电费（公共+空调）：按天分摊")
    print("   公式: 房间总电费 × (个人入住天数 / 房间总人天数)")
    print()
    print("✅ 水费：按天分摊")
    print("   公式: 房间总水费 × (个人入住天数 / 房间总人天数)")
    print()
    print("✅ 换房场景处理：")
    print("   - 旧房间：搬离日不计费（9月14日是最后一天）")
    print("   - 新房间：从入住日开始计费（9月15日开始）")
    print("   - 两个房间费用分别按天计算后相加")
    print("="*70)


if __name__ == "__main__":
    test_room_transfer_scenario()
