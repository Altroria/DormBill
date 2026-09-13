import urllib.request
import json

# 测试基本路由
urls = [
    "http://localhost:8000/",
    "http://localhost:8000/api/v1/buildings",
    "http://localhost:8000/api/v1/meters-v2/combined?month=2026-09",
]

for url in urls:
    try:
        with urllib.request.urlopen(url) as response:
            print(f"OK {url} - Status: {response.status}")
    except Exception as e:
        print(f"FAIL {url} - Error: {e}")
