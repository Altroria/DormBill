import requests
import json

print("=== 测试前端修复 ===\n")

# 1. 查看当前状态
print("1. 查看当前状态...")
r = requests.get('http://localhost:8001/api/meters-v2/list-enhanced', params={
    'month': '2026-09',
    'building_id': 1,
    'room_no': '45'
})
room = r.json()['items'][0]
print(f"   本月读数: {room['main_current_reading']}")
print(f"   用电量: {room['main_total_degree']}")
print(f"   总电费: {room['main_total_fee']}")

# 2. 模拟前端发送请求（只改本月读数，不手动输入用电量和电费）
print("\n2. 模拟前端保存（本月读数=1700，用电量和电费=None）...")
r = requests.put('http://localhost:8001/api/meters-v2/batch-update', json={
    'month': '2026-09',
    'updates': [{
        'building_id': 1,
        'room_no': '45',
        'main_current_reading': 1700.0,
        'main_total_degree': None,  # 前端发送None，表示不手动输入
        'main_total_fee': None,     # 前端发送None，表示不手动输入
        'ac_meters': []
    }]
})
print(f"   状态: {r.status_code}")
print(f"   响应: {r.json()}")

# 3. 验证结果
print("\n3. 验证结果...")
r = requests.get('http://localhost:8001/api/meters-v2/list-enhanced', params={
    'month': '2026-09',
    'building_id': 1,
    'room_no': '45'
})
room = r.json()['items'][0]
print(f"   本月读数: {room['main_current_reading']}")
print(f"   上月读数: {room['main_previous_reading']}")
print(f"   用电量: {room['main_total_degree']}")
print(f"   总电费: {room['main_total_fee']}")

expected_degree = room['main_current_reading'] - room['main_previous_reading']
expected_fee = expected_degree * 0.49

if abs(room['main_total_degree'] - expected_degree) < 0.01 and abs(room['main_total_fee'] - expected_fee) < 0.01:
    print(f"\n   [成功] 自动计算正确!")
    print(f"   期望用电量: {expected_degree}, 实际: {room['main_total_degree']}")
    print(f"   期望总电费: {expected_fee}, 实际: {room['main_total_fee']}")
else:
    print(f"\n   [失败] 计算错误!")
    print(f"   期望用电量: {expected_degree}, 实际: {room['main_total_degree']}")
    print(f"   期望总电费: {expected_fee}, 实际: {room['main_total_fee']}")
