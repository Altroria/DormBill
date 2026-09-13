import urllib.request
import json

url = "http://localhost:8000/api/v1/meters-v2/combined?month=2026-09"

try:
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())
        print(f"Status: {response.status}")
        print(f"Total: {data['total']}")
        print(f"Items: {len(data['items'])}")
        if data['items']:
            print("\nFirst item:")
            print(json.dumps(data['items'][0], indent=2, ensure_ascii=False))
except Exception as e:
    print(f"Error: {e}")
