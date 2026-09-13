import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# 测试批量更新空调表
def test_batch_update_ac():
    month = "2026-09"
    
    # 准备批量更新数据
    updates = [
        {
            "room_id": 1,
            "ac_current_reading": 1250.5,
            "ac_meter_no": "AC001"
        },
        {
            "room_id": 2,
            "ac_current_reading": 980.3,
            "ac_meter_no": "AC002"
        }
    ]
    
    url = f"{BASE_URL}/meters-v2/ac-batch/{month}"
    print(f"Testing URL: {url}")
    
    response = requests.put(url, json=updates)
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    test_batch_update_ac()
