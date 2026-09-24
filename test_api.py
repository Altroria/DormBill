import requests

response = requests.get(
    "http://localhost:8000/api/meters-v2/list-enhanced",
    params={"month": "2026-09", "skip": 0, "limit": 500},
    headers={"appkey": "test-auth-key"}
)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")
