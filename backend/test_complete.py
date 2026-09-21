import requests
import json

def test_scenario(name, building_id, room_no, main_reading, main_degree, main_fee):
    """测试一个场景"""
    print(f"\n{'='*60}")
    print(f"测试场景: {name}")
    print(f"{'='*60}")
    
    # 1. 发送更新请求
    print(f"\n发送数据:")
    print(f"  本月读数: {main_reading}")
    print(f"  用电量: {main_degree}")
    print(f"  总电费: {main_fee}")
    
    r = requests.put('http://localhost:8001/api/meters-v2/batch-update', json={
        'month': '2026-09',
        'updates': [{
            'building_id': building_id,
            'room_no': room_no,
            'main_current_reading': main_reading,
            'main_total_degree': main_degree,
            'main_total_fee': main_fee,
            'ac_meters': []
        }]
    })
    
    if r.status_code != 200:
        print(f"\n[错误] 请求失败: {r.status_code}")
        return False
    
    # 2. 查询验证
    r = requests.get('http://localhost:8001/api/meters-v2/list-enhanced', params={
        'month': '2026-09',
        'building_id': building_id,
        'room_no': room_no
    })
    
    room = r.json()['items'][0]
    
    print(f"\n实际结果:")
    print(f"  上月读数: {room['main_previous_reading']}")
    print(f"  本月读数: {room['main_current_reading']}")
    print(f"  用电量: {room['main_total_degree']}")
    print(f"  总电费: {room['main_total_fee']}")
    
    return room

print("="*60)
print("电表录入功能完整测试")
print("="*60)

# 场景1: 只修改本月读数，用电量和电费自动计算
room = test_scenario(
    "场景1: 只修改本月读数（自动计算）",
    building_id=1,
    room_no='45',
    main_reading=1800.0,
    main_degree=None,  # 自动计算
    main_fee=None      # 自动计算
)

expected_degree = room['main_current_reading'] - room['main_previous_reading']
expected_fee = expected_degree * 0.60

if abs(room['main_total_degree'] - expected_degree) < 0.01:
    print(f"\n[OK] 用电量自动计算正确: {expected_degree} -> {room['main_total_degree']}")
else:
    print(f"\n[ERROR] 用电量计算错误: 期望 {expected_degree}, 实际 {room['main_total_degree']}")

if abs(room['main_total_fee'] - expected_fee) < 0.01:
    print(f"[OK] 总电费自动计算正确: {expected_fee} -> {room['main_total_fee']}")
else:
    print(f"[ERROR] 总电费计算错误: 期望 {expected_fee}, 实际 {room['main_total_fee']}")

# 场景2: 手动输入用电量，电费自动计算
room = test_scenario(
    "场景2: 手动输入用电量（电费自动计算）",
    building_id=1,
    room_no='45',
    main_reading=1800.0,
    main_degree=2000.0,  # 手动输入
    main_fee=None        # 自动计算
)

expected_fee = 2000.0 * 0.60

if abs(room['main_total_degree'] - 2000.0) < 0.01:
    print(f"\n[OK] 用电量手动输入生效: {room['main_total_degree']}")
else:
    print(f"\n[ERROR] 用电量手动输入失败: 期望 2000.0, 实际 {room['main_total_degree']}")

if abs(room['main_total_fee'] - expected_fee) < 0.01:
    print(f"[OK] 总电费基于手动用电量计算正确: {expected_fee} -> {room['main_total_fee']}")
else:
    print(f"[ERROR] 总电费计算错误: 期望 {expected_fee}, 实际 {room['main_total_fee']}")

# 场景3: 两者都手动输入
room = test_scenario(
    "场景3: 用电量和电费都手动输入",
    building_id=1,
    room_no='45',
    main_reading=1800.0,
    main_degree=2500.0,  # 手动输入
    main_fee=1500.0      # 手动输入
)

if abs(room['main_total_degree'] - 2500.0) < 0.01:
    print(f"\n[OK] 用电量手动输入生效: {room['main_total_degree']}")
else:
    print(f"\n[ERROR] 用电量手动输入失败: 期望 2500.0, 实际 {room['main_total_degree']}")

if abs(room['main_total_fee'] - 1500.0) < 0.01:
    print(f"[OK] 总电费手动输入生效: {room['main_total_fee']}")
else:
    print(f"[ERROR] 总电费手动输入失败: 期望 1500.0, 实际 {room['main_total_fee']}")

# 场景4: 恢复自动计算
room = test_scenario(
    "场景4: 修改本月读数后恢复自动计算",
    building_id=1,
    room_no='45',
    main_reading=2000.0,
    main_degree=None,  # 恢复自动计算
    main_fee=None      # 恢复自动计算
)

expected_degree = room['main_current_reading'] - room['main_previous_reading']
expected_fee = expected_degree * 0.60

if abs(room['main_total_degree'] - expected_degree) < 0.01:
    print(f"\n[OK] 用电量恢复自动计算: {expected_degree} -> {room['main_total_degree']}")
else:
    print(f"\n[ERROR] 用电量计算错误: 期望 {expected_degree}, 实际 {room['main_total_degree']}")

if abs(room['main_total_fee'] - expected_fee) < 0.01:
    print(f"[OK] 总电费恢复自动计算: {expected_fee} -> {room['main_total_fee']}")
else:
    print(f"[ERROR] 总电费计算错误: 期望 {expected_fee}, 实际 {room['main_total_fee']}")

print(f"\n{'='*60}")
print("测试完成！")
print(f"{'='*60}")
