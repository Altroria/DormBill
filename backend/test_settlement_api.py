import requests
import json

# 查询结算数据
r = requests.get('http://localhost:8001/api/settlements/list', params={
    'month': '2026-09',
    'water_mode': 'double'
})

print(f"状态码: {r.status_code}")
print(f"\n返回数据结构:")
data = r.json()
print(json.dumps(data, indent=2, ensure_ascii=False))

if 'items' in data and len(data['items']) > 0:
    print(f"\n第一条记录的电费字段:")
    first_item = data['items'][0]
    print(f"  electricity_fee: {first_item.get('electricity_fee', 'NOT FOUND')}")
    print(f"  ac_electricity_fee: {first_item.get('ac_electricity_fee', 'NOT FOUND')}")
    print(f"\n完整记录:")
    print(json.dumps(first_item, indent=2, ensure_ascii=False))
