import urllib.request
import json

url = "http://localhost:8000/api/v1/meters-v2/init-month"
data = {
    "month": "2026-09",
    "building_id": 1
}

req = urllib.request.Request(
    url,
    data=json.dumps(data).encode('utf-8'),
    headers={'Content-Type': 'application/json'},
    method='POST'
)

try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        print(f"Status: {response.status}")
        print(f"Result: {json.dumps(result, indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"Error: {e}")
