import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_get_combined():
    """获取组合数据并查看45号房的空调表"""
    url = f"{BASE_URL}/meters-v2/combined"
    params = {
        "month": "2026-09",
        "room_no": "45"
    }
    
    response = requests.get(url, params=params)
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    test_get_combined()
