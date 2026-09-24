"""测试免租天数计算逻辑"""
from datetime import date
from app.utils.date_utils import get_free_rent_days_in_month, add_months

def test_scenario_1():
    """场景1：6月15日入住，3个月免租"""
    print("\n=== 场景1：6月15日入住，勾选前3个月免租 ===")
    check_in = date(2026, 6, 15)
    probation_months = 3
    probation_end = add_months(check_in, probation_months)
    print(f"入住日期: {check_in}")
    print(f"免租期结束: {probation_end} (不含当天)")
    
    test_months = [
        date(2026, 6, 1),
        date(2026, 7, 1),
        date(2026, 8, 1),
        date(2026, 9, 1),
        date(2026, 10, 1),
    ]
    
    for month in test_months:
        free_days = get_free_rent_days_in_month(check_in, probation_months, month)
        # 计算当月总天数
        if month.month == 6:
            total_days = 30
            stay_days = 16  # 15-30
        elif month.month == 7:
            total_days = 31
            stay_days = 31
        elif month.month == 8:
            total_days = 31
            stay_days = 31
        elif month.month == 9:
            total_days = 30
            stay_days = 30
        else:
            total_days = 31
            stay_days = 31
        
        chargeable_days = stay_days - free_days
        rent = 600 * chargeable_days / total_days if chargeable_days > 0 else 0
        
        print(f"{month.strftime('%Y-%m')}: 入住{stay_days}天, 免租{free_days}天, 计费{chargeable_days}天, 房租¥{rent:.2f}")

def test_scenario_2():
    """场景2：7月1日入住，3个月免租"""
    print("\n=== 场景2：7月1日入住，勾选前3个月免租 ===")
    check_in = date(2026, 7, 1)
    probation_months = 3
    probation_end = add_months(check_in, probation_months)
    print(f"入住日期: {check_in}")
    print(f"免租期结束: {probation_end} (不含当天)")
    
    test_months = [
        date(2026, 7, 1),
        date(2026, 8, 1),
        date(2026, 9, 1),
        date(2026, 10, 1),
    ]
    
    for month in test_months:
        free_days = get_free_rent_days_in_month(check_in, probation_months, month)
        if month.month == 7:
            total_days = 31
            stay_days = 31
        elif month.month == 8:
            total_days = 31
            stay_days = 31
        elif month.month == 9:
            total_days = 30
            stay_days = 30
        else:
            total_days = 31
            stay_days = 31
        
        chargeable_days = stay_days - free_days
        rent = 600 * chargeable_days / total_days if chargeable_days > 0 else 0
        
        print(f"{month.strftime('%Y-%m')}: 入住{stay_days}天, 免租{free_days}天, 计费{chargeable_days}天, 房租¥{rent:.2f}")

def test_scenario_3():
    """场景3：8月20日入住，不勾选免租"""
    print("\n=== 场景3：8月20日入住，不勾选免租 ===")
    check_in = date(2026, 8, 20)
    probation_months = 0
    print(f"入住日期: {check_in}")
    print(f"免租期: 无")
    
    test_months = [
        date(2026, 8, 1),
        date(2026, 9, 1),
        date(2026, 10, 1),
    ]
    
    for month in test_months:
        free_days = get_free_rent_days_in_month(check_in, probation_months, month)
        if month.month == 8:
            total_days = 31
            stay_days = 12  # 20-31
        elif month.month == 9:
            total_days = 30
            stay_days = 30
        else:
            total_days = 31
            stay_days = 31
        
        chargeable_days = stay_days - free_days
        rent = 600 * chargeable_days / total_days if chargeable_days > 0 else 0
        
        print(f"{month.strftime('%Y-%m')}: 入住{stay_days}天, 免租{free_days}天, 计费{chargeable_days}天, 房租¥{rent:.2f}")

def test_scenario_4():
    """场景4：6月15日入住并免租，8月20日搬离"""
    print("\n=== 场景4：6月15日入住免租，8月20日搬离 ===")
    check_in = date(2026, 6, 15)
    check_out = date(2026, 8, 20)
    probation_months = 3
    probation_end = add_months(check_in, probation_months)
    print(f"入住日期: {check_in}")
    print(f"搬离日期: {check_out}")
    print(f"免租期结束: {probation_end} (不含当天)")
    
    test_months = [
        date(2026, 6, 1),
        date(2026, 7, 1),
        date(2026, 8, 1),
        date(2026, 9, 1),
    ]
    
    for month in test_months:
        free_days = get_free_rent_days_in_month(check_in, probation_months, month)
        # 计算实际入住天数（考虑搬离）
        from app.utils.date_utils import stay_days_in_month
        stay_days = stay_days_in_month(check_in, check_out, month)
        
        if stay_days == 0:
            print(f"{month.strftime('%Y-%m')}: 未入住")
            continue
        
        chargeable_days = max(0, stay_days - free_days)
        if month.month == 6:
            total_days = 30
        elif month.month == 7:
            total_days = 31
        else:
            total_days = 31
        
        rent = 600 * chargeable_days / total_days if chargeable_days > 0 else 0
        
        print(f"{month.strftime('%Y-%m')}: 入住{stay_days}天, 免租{free_days}天, 计费{chargeable_days}天, 房租¥{rent:.2f}")

if __name__ == "__main__":
    print("=" * 60)
    print("前3个月免房租功能测试")
    print("=" * 60)
    
    test_scenario_1()
    test_scenario_2()
    test_scenario_3()
    test_scenario_4()
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)
