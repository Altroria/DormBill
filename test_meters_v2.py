"""测试电表V2 API"""
import requests
import json

def test_combined_meters():
    url = "http://localhost:8000/api/v1/meters-v2/combined"
    params = {
        "month": "2026-09",
        "limit": 5
    }
    
    try:
        response = requests.get(url, params=params)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        print(f"Response Text: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✓ Success!")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(f"\n✗ Error!")
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_combined_meters()
