"""
从 Excel 文件生成数据库导入 SQL
解析 7月份的 Excel 数据，生成楼栋、房间、员工的 SQL 插入脚本
"""
from openpyxl import load_workbook
from datetime import datetime
import os

def clean_value(value):
    """清理 Excel 单元格值"""
    if value is None:
        return None
    if isinstance(value, str):
        return value.strip()
    return value

def generate_import_sql():
    """生成完整的导入 SQL"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 读取员工扣款文件
    employee_file = os.path.join(base_dir, "7月宿舍员工 扣款.xlsx")
    wb = load_workbook(employee_file, data_only=True)
    ws = wb['Sheet1']
    
    # 用于去重
    buildings_set = set()
    rooms_dict = {}  # key: (building_no, room_no), value: room_info
    employees_dict = {}  # key: employee_no, value: employee_info
    
    print("正在解析数据...")
    
    # 用于记住上一个非空的楼号和房号（处理合并单元格）
    last_building_no = None
    last_room_no = None
    
    # 从第3行开始读取数据（第1行是表头，第2行是空行）
    for row_idx in range(3, ws.max_row + 1):
        row = ws[row_idx]
        
        # 读取各列数据
        building_no = clean_value(row[0].value)  # 楼号
        room_no = clean_value(row[1].value)      # 房号
        room_name = clean_value(row[5].value)    # 房间名称
        company = clean_value(row[6].value)      # 任职单位
        department = clean_value(row[7].value)   # 一级部门
        position = clean_value(row[8].value)     # 职务
        name = clean_value(row[9].value)         # 姓名
        
        # 处理合并单元格：如果当前行的楼号或房号为空，使用上一行的值
        if building_no:
            last_building_no = building_no
        else:
            building_no = last_building_no
            
        if room_no:
            last_room_no = room_no
        else:
            room_no = last_room_no
        
        # 跳过空行
        if not name:
            continue
        
        # 收集楼栋
        if building_no:
            buildings_set.add(building_no)
        
        # 收集房间（只在楼号和房号都有值时）
        if building_no and room_no and room_name:
            room_key = (building_no, room_no)
            if room_key not in rooms_dict:
                rooms_dict[room_key] = {
                    'building_no': building_no,
                    'room_no': room_no,
                    'name': room_name
                }
        
        # 收集员工
        if name and company:
            # 生成员工编号（简单方式：使用姓名的拼音首字母+随机数）
            # 这里先用姓名作为唯一标识
            employee_key = name
            if employee_key not in employees_dict:
                employees_dict[employee_key] = {
                    'name': name,
                    'company': company,
                    'department': department,
                    'position': position,
                    'building_no': building_no,
                    'room_no': room_no
                }
    
    wb.close()
    
    # 生成 SQL
    sql_lines = []
    sql_lines.append("-- 7月份数据导入脚本")
    sql_lines.append("-- 生成时间: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    sql_lines.append("")
    sql_lines.append("USE dormbill;")
    sql_lines.append("")
    
    # 1. 插入楼栋数据
    sql_lines.append("-- ======================================")
    sql_lines.append("-- 1. 插入楼栋数据")
    sql_lines.append("-- ======================================")
    for building_no in sorted(buildings_set, key=lambda x: str(x)):
        sql_lines.append(
            f"INSERT INTO buildings (building_no, name, status, created_at, updated_at) "
            f"VALUES ('{building_no}', '{building_no}栋', 'active', NOW(), NOW()) "
            f"ON DUPLICATE KEY UPDATE updated_at=NOW();"
        )
    sql_lines.append("")
    
    # 2. 插入房间数据
    sql_lines.append("-- ======================================")
    sql_lines.append("-- 2. 插入房间数据")
    sql_lines.append("-- ======================================")
    for room_key in sorted(rooms_dict.keys(), key=lambda x: (str(x[0]), str(x[1]))):
        room = rooms_dict[room_key]
        # 房间类型判断
        room_type = 'single'
        if '隔间' in room['name'] or '客隔' in room['name']:
            room_type = 'shared'
        elif '双人' in room['name']:
            room_type = 'double'
        elif '独卫' in room['name']:
            room_type = 'ensuite'
        
        sql_lines.append(
            f"INSERT INTO rooms (building_id, room_no, name, room_type, status, created_at, updated_at) "
            f"SELECT b.id, '{room['room_no']}', '{room['name']}', '{room_type}', 'available', NOW(), NOW() "
            f"FROM buildings b WHERE b.building_no = '{room['building_no']}' "
            f"ON DUPLICATE KEY UPDATE updated_at=NOW();"
        )
    sql_lines.append("")
    
    # 3. 插入员工数据
    sql_lines.append("-- ======================================")
    sql_lines.append("-- 3. 插入员工数据")
    sql_lines.append("-- ======================================")
    employee_no_counter = 1
    for employee_key in sorted(employees_dict.keys()):
        emp = employees_dict[employee_key]
        employee_no = f"E{employee_no_counter:04d}"
        employee_no_counter += 1
        
        # 处理可能为 None 的值
        company = emp.get('company') or '未知'
        department = emp.get('department') or ''
        position = emp.get('position') or ''
        
        sql_lines.append(
            f"INSERT INTO employees (employee_no, name, company, department, position, status, created_at, updated_at) "
            f"VALUES ('{employee_no}', '{emp['name']}', '{company}', '{department}', '{position}', 'active', NOW(), NOW()) "
            f"ON DUPLICATE KEY UPDATE updated_at=NOW();"
        )
    sql_lines.append("")
    
    # 保存到文件
    output_file = os.path.join(base_dir, "scripts", "import_july_data.sql")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(sql_lines))
    
    print(f"\n✅ SQL 文件已生成: {output_file}")
    print(f"\n统计信息:")
    print(f"  - 楼栋数量: {len(buildings_set)}")
    print(f"  - 房间数量: {len(rooms_dict)}")
    print(f"  - 员工数量: {len(employees_dict)}")
    print(f"\n楼栋列表: {sorted(buildings_set, key=lambda x: str(x))}")

if __name__ == "__main__":
    generate_import_sql()
