"""
测试V2重构功能的完整工作流

测试场景：
1. 初始化月度电表
2. 批量录入总表和空调表数据
3. 执行增强计算（公共用电 + 个人分摊）
4. 查询增强列表（验证统计数据）
5. 生成结算（使用V2架构）
"""
import requests
from decimal import Decimal
from datetime import datetime

# API基础URL
BASE_URL = "http://localhost:8000/api/v1"

# 测试月份
TEST_MONTH = "2026-09"


def test_init_month():
    """测试：初始化月度电表"""
    print("=" * 60)
    print("步骤1：初始化月度电表")
    print("=" * 60)
    
    url = f"{BASE_URL}/meters-v2/init-month"
    data = {
        "month": TEST_MONTH,
        "building_id": 1  # 指定楼栋
    }
    
    response = requests.post(url, json=data)
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✓ 初始化成功")
        print(f"  - 总表创建: {result.get('main_meters_created', 0)} 条")
        print(f"  - 空调表创建: {result.get('ac_meters_created', 0)} 条")
        return True
    else:
        print(f"✗ 初始化失败: {response.text}")
        return False


def test_batch_update():
    """测试：批量更新电表数据"""
    print("\n" + "=" * 60)
    print("步骤2：批量更新电表数据")
    print("=" * 60)
    
    url = f"{BASE_URL}/meters-v2/batch-update"
    
    # 模拟201房号的数据
    data = {
        "month": TEST_MONTH,
        "updates": [
            {
                "building_id": 1,
                "room_no": "201",
                "main_current_reading": 15000.5,  # 总表读数
                "main_meter_no": "M-201",
                "ac_meters": [
                    {"room_id": 1, "ac_current_reading": 1200.0},  # 201-1套间
                    {"room_id": 2, "ac_current_reading": 1350.0},  # 201-2套间
                    {"room_id": 3, "ac_current_reading": 1120.0},  # 201-3套间
                    {"room_id": 4, "ac_current_reading": 980.0},   # 201-4套间
                ]
            },
            {
                "building_id": 1,
                "room_no": "202",
                "main_current_reading": 13500.0,
                "main_meter_no": "M-202",
                "ac_meters": [
                    {"room_id": 5, "ac_current_reading": 950.0},
                    {"room_id": 6, "ac_current_reading": 1100.0},
                ]
            }
        ]
    }
    
    response = requests.put(url, json=data)
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✓ 批量更新成功")
        print(f"  - 总表更新: {result.get('main_meters_updated', 0)} 个房号")
        print(f"  - 空调表更新: {result.get('ac_meters_updated', 0)} 个套间")
        return True
    else:
        print(f"✗ 批量更新失败: {response.text}")
        return False


def test_enhanced_calculate():
    """测试：增强计算（公共用电 + 个人分摊）"""
    print("\n" + "=" * 60)
    print("步骤3：执行增强计算")
    print("=" * 60)
    
    url = f"{BASE_URL}/meters-v2/calculate-enhanced"
    data = {
        "month": TEST_MONTH,
        "building_id": 1,
        "calculate_distribution": True
    }
    
    response = requests.post(url, json=data)
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✓ 计算成功")
        print(f"  - 总表计算: {result.get('main_meters_calculated', 0)} 条")
        print(f"  - 空调表计算: {result.get('ac_meters_calculated', 0)} 条")
        print(f"  - 个人分摊: {result.get('distributions_created', 0)} 条")
        print(f"  - 公共电费总计: ¥{result.get('total_common_fee', 0):.2f}")
        print(f"  - 空调电费总计: ¥{result.get('total_ac_fee', 0):.2f}")
        return True
    else:
        print(f"✗ 计算失败: {response.text}")
        return False


def test_enhanced_list():
    """测试：查询增强列表"""
    print("\n" + "=" * 60)
    print("步骤4：查询增强列表（验证统计数据）")
    print("=" * 60)
    
    url = f"{BASE_URL}/meters-v2/list-enhanced"
    params = {
        "month": TEST_MONTH,
        "building_id": 1,
        "limit": 10
    }
    
    response = requests.get(url, params=params)
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        items = result.get('items', [])
        total = result.get('total', 0)
        
        print(f"✓ 查询成功，共 {total} 条记录\n")
        
        for item in items[:3]:  # 只显示前3条
            print(f"房号: {item['room_no']}")
            print(f"  总表: {item['main_total_degree']:.2f}度 / ¥{item['main_total_fee']:.2f}")
            print(f"  空调: {item['total_ac_degree']:.2f}度 / ¥{item['total_ac_fee']:.2f}")
            print(f"  公共用电: {item['common_degree']:.2f}度 / ¥{item['common_fee']:.2f}")
            print(f"  入住人数: {item['total_occupants']}人")
            print(f"  人均公共电费: ¥{item['common_fee_per_person']:.2f}")
            print(f"  套间数: {len(item['ac_meters'])} 个")
            
            for ac in item['ac_meters']:
                print(f"    - 套间{ac['room_unit']}: {ac['ac_degree']:.2f}度, "
                      f"¥{ac['ac_fee']:.2f}, {ac['occupants']}人")
            print()
        
        return True
    else:
        print(f"✗ 查询失败: {response.text}")
        return False


def test_settlement_generation():
    """测试：生成结算（使用V2架构）"""
    print("\n" + "=" * 60)
    print("步骤5：生成月度结算（使用V2电表数据）")
    print("=" * 60)
    
    url = f"{BASE_URL}/settlements/generate"
    data = {
        "month": TEST_MONTH,
        "use_v2": True  # 使用V2架构
    }
    
    response = requests.post(url, json=data)
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✓ 结算生成成功")
        print(f"  - 生成记录数: {len(result.get('items', []))} 条")
        
        # 显示前3条结算记录
        items = result.get('items', [])
        for item in items[:3]:
            print(f"\n  员工ID: {item.get('employee_id')}")
            print(f"    房租: ¥{item.get('rent_actual', 0):.2f}")
            print(f"    普通电费（公共电费）: ¥{item.get('electricity_fee', 0):.2f}")
            print(f"    空调电费: ¥{item.get('ac_electricity_fee', 0):.2f}")
            print(f"    水费: ¥{item.get('water_fee', 0):.2f}")
            print(f"    总计: ¥{item.get('total_amount', 0):.2f}")
        
        return True
    else:
        print(f"✗ 结算生成失败: {response.text}")
        return False


def run_full_workflow():
    """运行完整工作流测试"""
    print("\n" + "=" * 60)
    print("电表管理V2重构 - 完整工作流测试")
    print("=" * 60)
    print(f"测试月份: {TEST_MONTH}")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    results = []
    
    # 步骤1：初始化
    results.append(("初始化月度电表", test_init_month()))
    
    # 步骤2：批量更新
    results.append(("批量更新电表", test_batch_update()))
    
    # 步骤3：增强计算
    results.append(("增强计算", test_enhanced_calculate()))
    
    # 步骤4：查询列表
    results.append(("查询增强列表", test_enhanced_list()))
    
    # 步骤5：生成结算
    results.append(("生成结算", test_settlement_generation()))
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    for name, success in results:
        status = "✓ 通过" if success else "✗ 失败"
        print(f"{status} - {name}")
    
    total = len(results)
    passed = sum(1 for _, success in results if success)
    
    print(f"\n总计: {passed}/{total} 通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！V2重构功能正常工作。")
    else:
        print(f"\n⚠️ 有 {total - passed} 个测试失败，请检查。")


if __name__ == "__main__":
    run_full_workflow()
