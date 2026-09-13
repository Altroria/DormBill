import urllib.request
import json

url = "http://localhost:8000/api/v1/meters-v2/combined?month=2026-09&building_id=1"

try:
    with urllib.request.urlopen(url) as response:
        result = json.loads(response.read().decode('utf-8'))
        print(f"Status: {response.status}")
        print(f"Total: {result['total']}")
        print(f"Items: {len(result['items'])}")
        print("\n前3条记录:")
        for item in result['items'][:3]:
            print(f"\n房号: {item['room_no']}")
            print(f"  总表: {item['main_previous_reading']} -> {item['main_current_reading']}, 用电: {item['main_total_degree']}, 费用: {item['main_total_fee']}")
            print(f"  空调表数量: {len(item['ac_meters'])}")
            for ac in item['ac_meters']:
                print(f"    {ac['room_unit']}: {ac['ac_previous_reading']} -> {ac['ac_current_reading']}, 用电: {ac['ac_degree']}, 费用: {ac['ac_fee']}")
except Exception as e:
    print(f"Error: {e}")
