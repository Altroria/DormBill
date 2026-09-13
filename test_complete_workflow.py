"""
完整工作流测试：
1. 获取电表列表
2. 批量更新空调表
3. 验证更新结果
"""
import requests
import json
from datetime import datetime
import sys
import io

# 设置输出编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_URL = "http://localhost:8000/api/v1"

def test_workflow():
    month = "2026-09"
    building_id = 1
    
    print("=" * 60)
    print("测试完整工作流")
    print("=" * 60)
    
    # Step 1: 获取电表列表
    print("\n[Step 1] 获取电表列表...")
    url = f"{BASE_URL}/meters-v2/combined"
    params = {
        "month": month,
        "building_id": building_id,
        "skip": 0,
        "limit": 5
    }
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"❌ 获取失败: {response.status_code}")
        return
    
    data = response.json()
    print(f"✅ 获取成功，共 {data['total']} 条记录")
    
    if len(data['items']) == 0:
        print("❌ 没有数据")
        return
    
    # 显示第一个房间信息
    first_room = data['items'][0]
    print(f"\n房号: {first_room['room_no']}")
    print(f"总表读数: {first_room['main_current_reading']}")
    print(f"空调表数量: {len(first_room['ac_meters'])}")
    
    # Step 2: 准备批量更新数据
    print("\n[Step 2] 准备批量更新空调表...")
    updates = []
    
    for item in data['items'][:2]:  # 只更新前2个房间
        for ac_meter in item['ac_meters'][:2]:  # 每个房间只更新前2个空调表
            update_data = {
                "room_id": ac_meter['room_id'],
                "current_reading": ac_meter['ac_current_reading'] + 100.5,  # 增加100.5度
                "meter_no": f"AC-TEST-{ac_meter['room_id']}"
            }
            updates.append(update_data)
            print(f"  - Room {ac_meter['room_id']}: {ac_meter['ac_current_reading']} -> {update_data['current_reading']}")
    
    # Step 3: 批量更新
    print(f"\n[Step 3] 批量更新 {len(updates)} 条记录...")
    url = f"{BASE_URL}/meters-v2/ac-batch/{month}"
    response = requests.put(url, json=updates)
    
    if response.status_code != 200:
        print(f"❌ 更新失败: {response.status_code}")
        print(response.text)
        return
    
    result = response.json()
    print(f"✅ {result['message']}")
    
    # Step 4: 验证更新结果
    print("\n[Step 4] 验证更新结果...")
    response = requests.get(f"{BASE_URL}/meters-v2/combined", params=params)
    data = response.json()
    
    updated_count = 0
    for item in data['items'][:2]:
        for ac_meter in item['ac_meters']:
            if ac_meter['ac_meter_no'] and ac_meter['ac_meter_no'].startswith('AC-TEST-'):
                updated_count += 1
                print(f"  ✅ Room {ac_meter['room_id']}: " +
                      f"读数={ac_meter['ac_current_reading']}, " +
                      f"用量={ac_meter['ac_degree']}, " +
                      f"电费={ac_meter['ac_fee']}")
    
    print(f"\n验证完成，共 {updated_count} 条记录更新成功")
    
    # Step 5: 统计信息
    print("\n[Step 5] 统计信息...")
    total_degree = sum(
        ac['ac_degree'] 
        for item in data['items'] 
        for ac in item['ac_meters']
    )
    total_fee = sum(
        ac['ac_fee'] 
        for item in data['items'] 
        for ac in item['ac_meters']
    )
    
    print(f"总用电量: {total_degree:.2f} 度")
    print(f"总电费: {total_fee:.2f} 元")
    
    print("\n" + "=" * 60)
    print("✅ 工作流测试完成！")
    print("=" * 60)

if __name__ == "__main__":
    test_workflow()
