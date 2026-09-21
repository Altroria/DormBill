import requests
import json

print("=== 测试手动输入用电量 ===\n")

# 1. 测试手动输入用电量（覆盖自动计算）
print("1. 手动输入用电量=2000...")
r = requests.put('http://localhost:8001/api/meters-v2/batch-update', json={
    'month': '2026-09',
    'updates': [{
        'building_id': 1,
        'room_no': '45',
        'main_current_reading': 1700.0,
        'main_total_degree': 2000.0,  # 手动输入，覆盖自动计算
        'main_total_fee': None,       # 总电费仍然自动计算
        'ac_meters': []
    }]
})
print(f"   状态: {r.status_code}")

# 2. 验证结果
print("\n2. 验证结果...")
r = requests.get('http://localhost:8001/api/meters-v2/list-enhanced', params={
    'month': '2026-09',
    'building_id': 1,
    'room_no': '45'
})
room = r.json()['items'][0]
print(f"   本月读数: {room['main_current_reading']}")
print(f"   用电量: {room['main_total_degree']} (手动输入的2000)")
print(f"   总电费: {room['main_total_fee']} (基于2000自动计算)")

expected_fee = 2000.0 * 0.49
if abs(room['main_total_degree'] - 2000.0) < 0.01 and abs(room['main_total_fee'] - expected_fee) < 0.01:
    print(f"\n   [成功] 手动输入有效!")
else:
    print(f"\n   [失败] 手动输入无效")

# 3. 测试两者都手动输入
print("\n3. 手动输入用电量和总电费...")
r = requests.put('http://localhost:8001/api/meters-v2/batch-update', json={
    'month': '2026-09',
    'updates': [{
        'building_id': 1,
        'room_no': '45',
        'main_current_reading': 1700.0,
        'main_total_degree': 2500.0,  # 手动输入
        'main_total_fee': 1500.0,     # 手动输入
        'ac_meters': []
    }]
})
print(f"   状态: {r.status_code}")

# 4. 验证结果
print("\n4. 验证结果...")
r = requests.get('http://localhost:8001/api/meters-v2/list-enhanced', params={
    'month': '2026-09',
    'building_id': 1,
    'room_no': '45'
})
room = r.json()['items'][0]
print(f"   用电量: {room['main_total_degree']} (手动输入的2500)")
print(f"   总电费: {room['main_total_fee']} (手动输入的1500)")

if abs(room['main_total_degree'] - 2500.0) < 0.01 and abs(room['main_total_fee'] - 1500.0) < 0.01:
    print(f"\n   [成功] 两者都手动输入有效!")
else:
    print(f"\n   [失败] 手动输入无效")

# 5. 恢复自动计算
print("\n5. 恢复自动计算...")
r = requests.put('http://localhost:8001/api/meters-v2/batch-update', json={
    'month': '2026-09',
    'updates': [{
        'building_id': 1,
        'room_no': '45',
        'main_current_reading': 1700.0,
        'main_total_degree': None,
        'main_total_fee': None,
        'ac_meters': []
    }]
})
print(f"   状态: {r.status_code}")

r = requests.get('http://localhost:8001/api/meters-v2/list-enhanced', params={
    'month': '2026-09',
    'building_id': 1,
    'room_no': '45'
})
room = r.json()['items'][0]
print(f"   用电量: {room['main_total_degree']} (自动计算)")
print(f"   总电费: {room['main_total_fee']} (自动计算)")
