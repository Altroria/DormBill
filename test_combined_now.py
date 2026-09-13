import requests
import json

url = "http://localhost:8000/api/v1/meters-v2/combined"
params = {
    "month": "2026-09",
    "skip": 0,
    "limit": 10
}

try:
    response = requests.get(url, params=params)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
except Exception as e:
    print(f"Error: {e}")
