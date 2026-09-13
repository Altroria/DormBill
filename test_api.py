#!/usr/bin/env python3
"""查看房间数据结构"""
import urllib.request
import urllib.parse
import json

# 获取所有房间数据
params = {
    'skip': 0,
    'limit': 100
}

url = 'http://localhost:8000/api/rooms?' + urllib.parse.urlencode(params)

try:
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
        items = data.get('items', [])
        
        print(f"总记录数: {data.get('total')}")
        print(f"\n查看房间结构（前20条）:")
        print(f"{'楼栋':<8} {'房号':<10} {'室号':<10} {'房间名称':<20} {'总电表':<15} {'空调电表':<15}")
        print("-" * 100)
        
        for item in items[:20]:
            building_no = item.get('building_no', '-')
            room_no = item.get('room_no', '-')
            room_unit = item.get('room_unit', '-') or '-'
            room_name = item.get('room_name', '-')
            meter_no = item.get('meter_no', '-') or '-'
            ac_meter_no = item.get('ac_meter_no', '-') or '-'
            
            print(f"{building_no:<8} {room_no:<10} {room_unit:<10} {room_name:<20} {meter_no:<15} {ac_meter_no:<15}")
            
except Exception as e:
    print(f"错误: {e}")
