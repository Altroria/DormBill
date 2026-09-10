"""从扣款Excel中提取房间数据并生成SQL"""
import openpyxl
from pathlib import Path

# 读取Excel文件
excel_path = Path(r"e:\cursor\DormBill\7月宿舍员工 扣款.xlsx")
wb = openpyxl.load_workbook(excel_path, data_only=True)
ws = wb.active

# 存储唯一的房间信息
rooms_dict = {}

# 当前房间信息（用于填充合并单元格）
current_building_no = None
current_room_no = None

# 遍历数据行（跳过表头和第一个空行）
for row_idx, row in enumerate(ws.iter_rows(min_row=3, values_only=True), start=3):
    if not row or not any(row):
        continue
    
    # 列索引：0-楼号, 1-房号, 4-室号, 5-房间
    building_no = str(row[0] or "").strip()
    room_no = str(row[1] or "").strip()
    room_unit = str(row[4] or "").strip()   # 室号在第4列
    room_name = str(row[5] or "").strip()   # 房间在第5列
    
    # 如果楼号和房号不为空，更新当前房间
    if building_no:
        current_building_no = building_no
    if room_no:
        current_room_no = room_no
    
    # 使用当前房间信息
    if current_building_no and current_room_no and room_unit:
        key = f"{current_building_no}-{current_room_no}-{room_unit}"
        
        if key not in rooms_dict:
            rooms_dict[key] = {
                'building_no': current_building_no,
                'room_no': current_room_no,
                'room_unit': room_unit,
                'room_name': room_name
            }

print(f"找到 {len(rooms_dict)} 个唯一房间\n")

# 输出房间列表
print("=" * 100)
print("房间列表：")
print("=" * 100)
for key, room in sorted(rooms_dict.items()):
    print(f"楼号: {room['building_no']:6s} | 房号: {room['room_no']:5s} | 室号: {room['room_unit']:5s} | 房间: {room['room_name']}")

print("\n" + "=" * 100)
print("SQL语句（用于更新room_unit字段）：")
print("=" * 100)

# 生成SQL更新语句
sql_statements = []
for key, room in sorted(rooms_dict.items()):
    building_no = room['building_no']
    room_no = room['room_no']
    room_unit = room['room_unit']
    room_name = room['room_name']
    
    sql = f"""UPDATE rooms r 
JOIN buildings b ON r.building_id = b.id 
SET r.room_unit = '{room_unit}', r.room_name = '{room_name}'
WHERE b.building_no = '{building_no}' AND r.room_no = '{room_no}';"""
    sql_statements.append(sql)

for sql in sql_statements:
    print(sql)
    print()

print(f"生成了 {len(sql_statements)} 条SQL更新语句")

# 保存到文件
output_file = Path(r"e:\cursor\DormBill\scripts\update_room_units.sql")
with open(output_file, 'w', encoding='utf-8') as f:
    for sql in sql_statements:
        f.write(sql + '\n\n')

print(f"\nSQL已保存到: {output_file}")
