"""测试 Meter V2 API"""
import requests
import json

base_url = "http://localhost:8000"

# 测试获取组合电表列表
def test_combined_meters():
    print("Testing GET /api/v1/meters-v2/combined")
    try:
        response = requests.get(
            f"{base_url}/api/v1/meters-v2/combined",
            params={
                "month": "2026-09",
                "limit": 5
            }
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"Error: {e}")
        print(f"Response text: {response.text if 'response' in locals() else 'No response'}")

if __name__ == "__main__":
    test_combined_meters()
