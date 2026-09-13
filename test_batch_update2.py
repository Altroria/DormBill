import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# 使用实际存在的room_id进行测试
def test_batch_update_ac():
    month = "2026-09"
    
    # 使用实际返回的room_id
    updates = [
        {
            "room_id": 92,  # 45-4
            "ac_current_reading": 1250.5,
            "ac_meter_no": "AC-45-4"
        },
        {
            "room_id": 91,  # 45-3
            "ac_current_reading": 980.3,
            "ac_meter_no": "AC-45-3"
        },
        {
            "room_id": 89,  # 45-1
            "ac_current_reading": 1100.0,
            "ac_meter_no": "AC-45-1"
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
