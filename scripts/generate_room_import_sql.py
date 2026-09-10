"""生成完整的房间数据导入SQL（INSERT + UPDATE）"""
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
    room_unit = str(row[4] or "").strip()
    room_name = str(row[5] or "").strip()
    
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

# 生成完整的SQL文件
output_file = Path(r"e:\cursor\DormBill\scripts\import_rooms_complete.sql")

with open(output_file, 'w', encoding='utf-8') as f:
    f.write("-- 房间数据导入SQL\n")
    f.write("-- 此SQL会先尝试更新，如果房间不存在则插入新记录\n\n")
    
    for key, room in sorted(rooms_dict.items()):
        building_no = room['building_no']
        room_no = room['room_no']
        room_unit = room['room_unit']
        room_name = room['room_name'].replace("'", "''")  # 转义单引号
        
        # 使用 INSERT ... ON DUPLICATE KEY UPDATE 或者先检查再插入
        sql = f"""-- {building_no}-{room_no}-{room_unit}
INSERT INTO rooms (building_id, room_no, room_unit, room_name, electricity_price, rent_standard, status)
SELECT b.id, '{room_no}', '{room_unit}', '{room_name}', 0.49, 0, 'active'
FROM buildings b
WHERE b.building_no = '{building_no}'
AND NOT EXISTS (
    SELECT 1 FROM rooms r2
    WHERE r2.building_id = b.id AND r2.room_no = '{room_no}' AND r2.room_unit = '{room_unit}'
);

UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_name = '{room_name}'
WHERE b.building_no = '{building_no}' AND r.room_no = '{room_no}' AND r.room_unit = '{room_unit}';

"""
        f.write(sql)

print(f"完整SQL已保存到: {output_file}")

# 同时生成一个纯UPDATE版本（用于已存在的房间）
output_file_update = Path(r"e:\cursor\DormBill\scripts\update_rooms_only.sql")

with open(output_file_update, 'w', encoding='utf-8') as f:
    f.write("-- 房间数据更新SQL（仅更新已存在的房间）\n\n")
    
    for key, room in sorted(rooms_dict.items()):
        building_no = room['building_no']
        room_no = room['room_no']
        room_unit = room['room_unit']
        room_name = room['room_name'].replace("'", "''")
        
        sql = f"""UPDATE rooms r
JOIN buildings b ON r.building_id = b.id
SET r.room_unit = '{room_unit}', r.room_name = '{room_name}'
WHERE b.building_no = '{building_no}' AND r.room_no = '{room_no}';

"""
        f.write(sql)

print(f"纯UPDATE版本已保存到: {output_file_update}")
