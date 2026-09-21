"""测试批量保存功能"""
import requests
import json

# API基础URL
BASE_URL = "http://localhost:8001/api"

# 测试数据
test_data = {
    "month": "2026-09",
    "updates": [
        {
            "building_id": 1,
            "room_no": "45",
            "main_current_reading": 1500.0,  # 假设修改本月读数为1500
            "main_total_degree": 0.0,         # 前端发送0
            "main_total_fee": 0.0,            # 前端发送0
            "ac_meters": []
        }
    ]
}

print("=== 测试批量保存功能 ===\n")
print("发送的数据:")
print(json.dumps(test_data, indent=2, ensure_ascii=False))
print()

# 先查询当前数据
print("1. 查询当前数据...")
response = requests.get(
    f"{BASE_URL}/meters-v2/list-enhanced",
    params={
        "month": "2026-09",
        "building_id": 1,
        "room_no": "45"
    }
)

if response.status_code == 200:
    data = response.json()
    if data["items"]:
        item = data["items"][0]
        print(f"   楼栋: {item['building_id']}, 房号: {item['room_no']}")
        print(f"   上月读数: {item['main_previous_reading']}")
        print(f"   本月读数: {item['main_current_reading']}")
        print(f"   用电量: {item['main_total_degree']}")
        print(f"   总电费: {item['main_total_fee']}")
    else:
        print("   没有数据")
else:
    print(f"   查询失败: {response.status_code}")
    print(f"   {response.text}")

print()

# 执行批量保存
print("2. 执行批量保存...")
response = requests.put(
    f"{BASE_URL}/meters-v2/batch-update",
    json=test_data
)

if response.status_code == 200:
    result = response.json()
    print(f"   [OK] {result['message']}")
else:
    print(f"   [ERROR] 保存失败: {response.status_code}")
    print(f"   {response.text}")

print()

# 再次查询验证
print("3. 验证保存结果...")
response = requests.get(
    f"{BASE_URL}/meters-v2/list-enhanced",
    params={
        "month": "2026-09",
        "building_id": 1,
        "room_no": "45"
    }
)

if response.status_code == 200:
    data = response.json()
    if data["items"]:
        item = data["items"][0]
        print(f"   楼栋: {item['building_id']}, 房号: {item['room_no']}")
        print(f"   上月读数: {item['main_previous_reading']}")
        print(f"   本月读数: {item['main_current_reading']}")
        print(f"   用电量: {item['main_total_degree']}")
        print(f"   总电费: {item['main_total_fee']}")
        
        # 验证是否自动计算
        expected_degree = item['main_current_reading'] - item['main_previous_reading']
        if abs(item['main_total_degree'] - expected_degree) < 0.01:
            print(f"\n   [OK] 用电量自动计算正确!")
            if item['main_total_fee'] > 0:
                print(f"   [OK] 总电费自动计算正确!")
            else:
                print(f"   [ERROR] 总电费为0，计算可能有问题")
        else:
            print(f"\n   [ERROR] 用电量计算错误，期望: {expected_degree}, 实际: {item['main_total_degree']}")
    else:
        print("   没有数据")
else:
    print(f"   查询失败: {response.status_code}")
