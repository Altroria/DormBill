"""测试空调表列表是否包含 room_name 字段"""
import requests
import json
from datetime import date

BASE_URL = "http://localhost:8001/api"

def test_room_name_in_ac_meters():
    """测试获取电表列表时空调表是否包含房间名"""
    print("=" * 60)
    print("测试：空调表列表是否包含 room_name 字段")
    print("=" * 60)
    
    # 获取2026年9月的电表数据
    month = "2026-09"
    building_id = 1
    
    url = f"{BASE_URL}/meters-v2/list-enhanced"
    params = {
        "month": month,
        "building_id": building_id,
        "limit": 10
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"[FAIL] API请求失败: {response.status_code}")
        print(response.text)
        return False
    
    data = response.json()
    
    print(f"返回记录数: {len(data.get('items', []))}")
    print()
    
    if not data.get('items'):
        print("[WARN] 没有找到记录，无法测试")
        return True
    
    # 检查第一条记录
    first_item = data['items'][0]
    print(f"房号: {first_item['building_id']}-{first_item['room_no']}")
    print(f"月份: {first_item['month']}")
    print(f"空调表数量: {len(first_item['ac_meters'])}")
    print()
    
    if not first_item['ac_meters']:
        print("[WARN] 该房号没有空调表记录")
        return True
    
    # 检查每个空调表是否包含 room_name
    all_passed = True
    for idx, ac_meter in enumerate(first_item['ac_meters'], 1):
        room_id = ac_meter.get('room_id')
        room_unit = ac_meter.get('room_unit')
        room_name = ac_meter.get('room_name')
        occupants = ac_meter.get('occupants', 0)
        
        print(f"空调表 {idx}:")
        print(f"  room_id: {room_id}")
        print(f"  room_unit: {room_unit}")
        print(f"  room_name: {room_name}")
        print(f"  occupants: {occupants}")
        
        if 'room_name' not in ac_meter:
            print(f"  [FAIL] 缺少 room_name 字段")
            all_passed = False
        else:
            print(f"  [PASS] room_name 字段存在")
        print()
    
    if all_passed:
        print("=" * 60)
        print("[SUCCESS] 所有空调表都包含 room_name 字段")
        print("=" * 60)
    else:
        print("=" * 60)
        print("[FAIL] 部分空调表缺少 room_name 字段")
        print("=" * 60)
    
    return all_passed

if __name__ == "__main__":
    try:
        test_room_name_in_ac_meters()
    except Exception as e:
        print(f"[ERROR] 测试失败: {e}")
        import traceback
        traceback.print_exc()
