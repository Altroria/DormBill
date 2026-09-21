"""检查上月读数"""
import requests

BASE_URL = "http://localhost:8001/api"

# 查询45号房间的历史数据
response = requests.get(
    f"{BASE_URL}/meters-v2/list-enhanced",
    params={
        "month": "2026-09",
        "building_id": 1,
        "room_no": "45",
    }
)

if response.status_code == 200:
    result = response.json()
    print("=== 45号房间历史数据 ===\n")
    for item in result['items']:
        print(f"月份: {item['month']}")
        print(f"  上月读数: {item['main_previous_reading']}")
        print(f"  本月读数: {item['main_current_reading']}")
        print(f"  用电量: {item['main_total_degree']}")
        print(f"  总电费: {item['main_total_fee']}")
        print()
else:
    print(f"查询失败: {response.status_code}")
    print(response.text)
