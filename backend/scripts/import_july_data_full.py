"""
完整导入7月份数据脚本
"""
import sys
from pathlib import Path

# 添加项目路径
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

import openpyxl
from datetime import datetime, date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.building import Building
from app.models.room import Room
from app.models.employee import Employee
from app.models.residence import ResidenceRecord
from app.models.meter import MeterRecord
from app.models.water import WaterExpense

# 数据库配置
DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '495648',
    'database': 'dormbill'
}

# 创建数据库连接
DATABASE_URL = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

def parse_room_number(room_str):
    """解析房间号，返回楼栋号和房间号"""
    if not room_str or not isinstance(room_str, (int, float, str)):
        return None, None
    
    room_str = str(int(float(room_str)))
    
    # 处理247xx格式: 247 = 2号楼4层7号房间基数
    # 实际上247开头表示2号楼,最后两位是房间号
    if len(room_str) == 3:
        # 例如: 201 = 2号楼01室
        building_num = room_str[0]     # 第一位是楼栋
        room_num = room_str[1:]        # 后两位是房间
        return building_num, room_num
    elif len(room_str) == 5:
        # 例如: 24701 = 2号楼01室 (247是楼层编码)
        building_num = room_str[0]     # 第一位是楼栋
        room_num = room_str[-2:]       # 最后两位是房间
        return building_num, room_num
    elif len(room_str) >= 4:
        # 例如: 2401 = 2号楼01室
        building_num = room_str[0]     # 第一位是楼栋
        room_num = room_str[-2:]       # 最后两位是房间
        return building_num, room_num
    
    return None, None

def get_or_create_building(session, building_num, building_name=None):
    """获取或创建楼栋"""
    if not building_num:
        return None
    
    building = session.query(Building).filter_by(building_no=building_num).first()
    if not building:
        building = Building(
            building_no=building_num,
            name=building_name or f"{building_num}号楼",
            status="active"
        )
        session.add(building)
        session.flush()
        print(f"  创建楼栋: {building.name}")
    return building

def get_or_create_room(session, building_id, room_num, household_num):
    """获取或创建房间"""
    if not building_id or not room_num:
        return None
    
    room = session.query(Room).filter_by(
        building_id=building_id,
        room_no=room_num
    ).first()
    
    if not room:
        room = Room(
            building_id=building_id,
            room_no=room_num,
            room_name=f"{room_num}室",
            status="active"
        )
        session.add(room)
        session.flush()
        print(f"  创建房间: {room_num}室")
    return room

def import_employee_data(session, file_path):
    """导入员工和入住数据"""
    print("\n" + "="*60)
    print("开始导入员工数据")
    print("="*60)
    
    wb = openpyxl.load_workbook(file_path)
    ws = wb.active
    
    imported_count = 0
    skipped_count = 0
    
    # 从第3行开始读取(跳过表头和空行)
    for row_idx, row in enumerate(ws.iter_rows(min_row=3, values_only=True), 3):
        building_room = row[0]  # 楼栋列
        room_col = row[1]       # 房间列
        household_num = row[4]  # 户号
        name = row[5]           # 姓名
        gender = row[6]         # 性别
        department = row[7]     # 任职单位
        position = row[8]       # 职务
        manager = row[9]        # 负责人
        notes = row[10]         # 转入转出日期
        total_fee = row[11]     # 电压床摊+水费+空调费
        expected_rent = row[12] # 应住宿费
        actual_payment = row[13] # 实缴费用
        
        # 跳过空行或无效行
        if not name or not household_num:
            continue
            
        try:
            # 解析楼栋和房间号
            building_num = None
            room_num = None
            
            # 优先使用第一列的楼栋房间信息
            if building_room:
                building_num, room_num = parse_room_number(building_room)
            
            # 如果第一列没有，使用第二列
            if not building_num and room_col:
                building_num, room_num = parse_room_number(room_col)
            
            if not building_num or not room_num:
                print(f"第{row_idx}行: 无法解析房间号 - {name}")
                skipped_count += 1
                continue
            
            # 获取或创建楼栋
            building = get_or_create_building(session, building_num)
            if not building:
                print(f"第{row_idx}行: 无法创建楼栋 - {name}")
                skipped_count += 1
                continue
            
            # 获取或创建房间
            room = get_or_create_room(session, building.id, room_num, household_num)
            if not room:
                print(f"第{row_idx}行: 无法创建房间 - {name}")
                skipped_count += 1
                continue
            
            # 检查员工是否已存在
            employee = session.query(Employee).filter_by(name=name).first()
            if not employee:
                # 生成工号
                employee_no = f"EMP{row_idx:04d}"
                
                # 创建员工
                employee = Employee(
                    employee_no=employee_no,
                    name=name,
                    company=department or "",
                    department=department or "",
                    position=position or "",
                    status="active"
                )
                session.add(employee)
                session.flush()
                print(f"第{row_idx}行: 创建员工 - {name} ({department})")
            
            # 检查入住记录是否已存在
            residence = session.query(ResidenceRecord).filter_by(
                employee_id=employee.id,
                room_id=room.id,
                check_out_date=None
            ).first()
            
            if not residence:
                # 创建入住记录
                residence = ResidenceRecord(
                    employee_id=employee.id,
                    room_id=room.id,
                    check_in_date=date(2026, 7, 1),  # 7月1日入住
                    status="valid"
                )
                session.add(residence)
                print(f"  入住: {building_num}栋{room_num}室")
            
            imported_count += 1
            
        except Exception as e:
            print(f"第{row_idx}行错误: {name} - {str(e)}")
            skipped_count += 1
            continue
    
    session.commit()
    print(f"\n员工数据导入完成: 成功 {imported_count} 条, 跳过 {skipped_count} 条")

def import_meter_data(session, file_path):
    """导入电表数据"""
    print("\n" + "="*60)
    print("开始导入电表数据")
    print("="*60)
    
    # data_only=True 获取公式计算后的值
    wb = openpyxl.load_workbook(file_path, data_only=True)
    ws = wb.active
    
    imported_count = 0
    skipped_count = 0
    
    # 从第3行开始读取
    for row_idx, row in enumerate(ws.iter_rows(min_row=3, values_only=True), 3):
        seq = row[0]            # 序号
        building_col = row[1]   # 楼栋号 (如247 = 2栋47室)
        room_col = row[2]       # 房间号 (如201,这是另一种编号)
        household_name = row[3] # 户主
        ac_usage_value = row[4] # 空调度数(已计算)
        
        # 跳过汇总行和空行
        if not isinstance(seq, (int, float)) or not building_col:
            continue
        
        try:
            # 247 = 2号楼47室, 248 = 2号楼48室
            building_str = str(int(float(building_col)))
            if len(building_str) >= 3:
                building_num = building_str[0]      # 第一位是楼栋号
                room_num = building_str[1:]         # 后面是房间号
            else:
                skipped_count += 1
                continue
            
            if not building_num or not room_num:
                skipped_count += 1
                continue
            
            # 查找楼栋
            building = session.query(Building).filter_by(building_no=building_num).first()
            if not building:
                print(f"第{row_idx}行: 找不到楼栋 {building_num} (原始:{building_col})")
                skipped_count += 1
                continue
            
            # 查找房间
            room = session.query(Room).filter_by(
                building_id=building.id,
                room_no=room_num
            ).first()
            
            if not room:
                print(f"第{row_idx}行: 找不到房间 {building_num}栋{room_num}室 (原始:{building_col})")
                skipped_count += 1
                continue
            
            # 获取空调度数
            if not ac_usage_value or not isinstance(ac_usage_value, (int, float)):
                skipped_count += 1
                continue
            
            ac_usage = float(ac_usage_value)
            
            if ac_usage <= 0:
                skipped_count += 1
                continue
            
            # 检查是否已存在该房间的7月电表记录
            existing = session.query(MeterRecord).filter_by(
                room_id=room.id,
                month=date(2026, 7, 1)
            ).first()
            
            if existing:
                # 更新已有记录的空调数据
                existing.ac_current_reading = ac_usage
                existing.ac_degree = ac_usage
                existing.ac_unit_price = 0.5
                existing.ac_fee = ac_usage * 0.5
                print(f"第{row_idx}行: {building_num}栋{room_num}室 ({household_name}) - 更新空调 {ac_usage:.1f}度")
            else:
                # 创建新的电表记录
                meter_record = MeterRecord(
                    room_id=room.id,
                    month=date(2026, 7, 1),  # 7月份
                    previous_reading=0.0,
                    current_reading=0.0,
                    total_degree=0.0,
                    ac_previous_reading=0.0,
                    ac_current_reading=ac_usage,
                    ac_degree=ac_usage,
                    electricity_price=0.49,
                    ac_unit_price=0.5,
                    total_fee=0.0,
                    ac_fee=ac_usage * 0.5,
                    status="normal"
                )
                session.add(meter_record)
                print(f"第{row_idx}行: {building_num}栋{room_num}室 ({household_name}) - {ac_usage:.1f}度")
            
            imported_count += 1
            
        except Exception as e:
            print(f"第{row_idx}行错误: {str(e)}")
            skipped_count += 1
            continue
    
    session.commit()
    print(f"\n电表数据导入完成: 成功 {imported_count} 条, 跳过 {skipped_count} 条")

def main():
    # 文件路径
    base_dir = Path(__file__).parent.parent.parent
    employee_file = base_dir / "7月宿舍员工 扣款.xlsx"
    ac_file = base_dir / "7月空调各房间分摊费用.xlsx"
    
    print("\n" + "="*60)
    print("7月份数据导入工具")
    print("="*60)
    
    # 检查文件
    if not employee_file.exists():
        print(f"错误: 找不到文件 {employee_file}")
        return
    
    if not ac_file.exists():
        print(f"错误: 找不到文件 {ac_file}")
        return
    
    # 创建数据库会话
    session = SessionLocal()
    
    try:
        # 导入员工和入住数据
        import_employee_data(session, employee_file)
        
        # 导入电表数据
        import_meter_data(session, ac_file)
        
        print("\n" + "="*60)
        print("所有数据导入完成!")
        print("="*60)
        
    except Exception as e:
        print(f"\n导入失败: {str(e)}")
        session.rollback()
        raise
    finally:
        session.close()

if __name__ == "__main__":
    main()
