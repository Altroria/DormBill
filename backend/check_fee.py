import requests

r = requests.get('http://localhost:8001/api/meters-v2/list-enhanced', params={
    'month': '2026-09',
    'building_id': 1,
    'room_no': '45'
})
room = r.json()['items'][0]
print(f'上月读数: {room["main_previous_reading"]}')
print(f'本月读数: {room["main_current_reading"]}')
print(f'用电量: {room["main_total_degree"]}')
print(f'总电费: {room["main_total_fee"]}')
print(f'预期电费(0.49): {room["main_total_degree"] * 0.49}')
print(f'预期电费(0.60): {room["main_total_degree"] * 0.60}')
