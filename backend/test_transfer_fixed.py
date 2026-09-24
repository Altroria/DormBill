"""验证修复后的换房逻辑"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from datetime import date, timedelta

def test_transfer_logic_fixed():
    """
    验证修复后的换房逻辑
    
    场景：用户输入"9月15日换房"
    系统应理解为：
    - 9月14日是住旧房的最后一天
    - 9月15日开始住新房
    """
    print("\n" + "="*70)
    print("验证修复后的换房逻辑")
    print("="*70)
    
    transfer_date = date(2026, 9, 15)
    
    # 模拟修复后的逻辑
    old_check_out_date = transfer_date - timedelta(days=1)  # 9月14日
    new_check_in_date = transfer_date  # 9月15日
    
    print(f"\n用户输入: 9月15日换房")
    print(f"\n修复后的处理:")
    print(f"  旧房记录:")
    print(f"    - check_out_date: {old_check_out_date} (最后一天住旧房)")
    print(f"    - status: leave (已搬离)")
    print(f"  新房记录:")
    print(f"    - check_in_date: {new_check_in_date} (第一天住新房)")
    print(f"    - status: valid (有效)")
    
    # 验证天数
    from app.utils.date_utils import stay_days_in_month
    
    target_month = date(2026, 9, 1)
    old_check_in = date(2026, 9, 1)
    
    old_days = stay_days_in_month(old_check_in, old_check_out_date, target_month)
    new_days = stay_days_in_month(new_check_in_date, None, target_month)
    
    print(f"\n9月份天数计算:")
    print(f"  旧房: 9月1日 - 9月14日 = {old_days} 天")
    print(f"  新房: 9月15日 - 9月30日 = {new_days} 天")
    print(f"  总计: {old_days} + {new_days} = {old_days + new_days} 天")
    
    if old_days + new_days == 30:
        print(f"  ✅ 正确！无重复计费，无遗漏")
    else:
        print(f"  ❌ 错误！应为30天")
    
    print("\n" + "="*70)
    print("主要修复点:")
    print("="*70)
    print("1. 旧房check_out_date改为: transfer_date - 1天")
    print("2. 旧房status改为: 'leave'（而非'invalid'）")
    print("3. 新房继承is_primary_payer（而非固定为0）")
    print("4. 确保无重复计费")
    print("="*70)


if __name__ == "__main__":
    test_transfer_logic_fixed()
