"""测试check_out_date的含义"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from datetime import date, timedelta
from app.utils.date_utils import stay_days_in_month

def test_check_out_date_meaning():
    """
    测试check_out_date的含义：
    - 是最后一天住的日期（包含）
    - 还是搬离的日期（不包含）
    """
    print("\n" + "="*70)
    print("测试 check_out_date 的含义")
    print("="*70)
    
    target_month = date(2026, 9, 1)
    check_in = date(2026, 9, 1)
    
    # 场景1: check_out_date = 9月14日
    check_out_1 = date(2026, 9, 14)
    days_1 = stay_days_in_month(check_in, check_out_1, target_month)
    
    print(f"\n场景1: 入住9月1日，check_out_date = 9月14日")
    print(f"  计算天数: {days_1} 天")
    print(f"  理解: check_out_date是最后一天（包含14日）" if days_1 == 14 else f"  理解: check_out_date是搬离日（不包含14日）")
    
    # 场景2: check_out_date = 9月15日
    check_out_2 = date(2026, 9, 15)
    days_2 = stay_days_in_month(check_in, check_out_2, target_month)
    
    print(f"\n场景2: 入住9月1日，check_out_date = 9月15日")
    print(f"  计算天数: {days_2} 天")
    print(f"  理解: check_out_date是最后一天（包含15日）" if days_2 == 15 else f"  理解: check_out_date是搬离日（不包含15日）")
    
    print("\n" + "="*70)
    print("结论:")
    print("="*70)
    print(f"当前实现中，check_out_date 的含义是：")
    print(f"  ✅ **最后一天入住的日期（包含这一天）**")
    print()
    print(f"换房场景示例（9月15日换房）：")
    print(f"  - 旧房记录: check_in=9月1日, check_out_date=9月14日")
    print(f"    → 住了1日到14日，共14天")
    print(f"  - 新房记录: check_in=9月15日, check_out_date=None")
    print(f"    → 住了15日到30日，共16天")
    print()
    print(f"当前换房接口的问题：")
    print(f"  ❌ 如果用户输入\"9月15日换房\"，系统应理解为：")
    print(f"     - 9月15日开始住新房")
    print(f"     - 9月14日是住旧房的最后一天")
    print(f"  ❌ 但当前代码设置: old_res.check_out_date = transfer_date")
    print(f"     这会导致：")
    print(f"     - 旧房: 1日-15日 (15天)")
    print(f"     - 新房: 15日-30日 (16天)")
    print(f"     - 15日重复计费！")
    print("="*70)


if __name__ == "__main__":
    test_check_out_date_meaning()
