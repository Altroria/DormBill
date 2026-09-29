"""
从房间和人员Excel导入/更新数据
支持直接覆盖更新房间、人员、入住信息
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

import xlrd
from datetime import date
from sqlalchemy import and_
from app.database import SessionLocal
from app.models import Building, Room, Employee, ResidenceRecord


def parse_building_and_room(building_str, room_str):
    """解析楼栋和房号"""
    building_no = str(building_str).strip()
    room_no = str(room_str).strip()
    
    # 移除.0后缀
    if building_no.endswith('.0'):
        building_no = building_no[:-2]
    if room_no.endswith('.0'):
        room_no = room_no[:-2]
    
    # 处理99楼的特殊情况（99-45 -> 99楼）
    if building_no.startswith('99'):
        building_no = '99'
    
    return building_no, room_no


def import_personnel_data(file_path, mode='update'):
    """
    导入房间和人员数据
    
    Args:
        file_path: Excel文件路径
        mode: 导入模式
            - 'update': 更新模式（默认），已存在则更新，不存在则创建
            - 'override': 覆盖模式，先清空所有入住记录，再重新导入
            - 'add_only': 仅添加模式，跳过已存在的记录
    """
    print(f"开始导入数据，模式: {mode}")
    print("=" * 80)
    
    wb = xlrd.open_workbook(file_path)
    ws = wb.sheet_by_index(0)
    
    db = SessionLocal()
    
    try:
        # 如果是覆盖模式，先清空入住记录
        if mode == 'override':
            print("\n清空现有入住记录...")
            deleted_count = db.query(ResidenceRecord).delete()
            db.commit()
            print(f"已删除 {deleted_count} 条入住记录")
        
        # 缓存
        building_cache = {}
        room_cache = {}
        employee_cache = {}
        
        # 统计
        stats = {
            'buildings_created': 0,
            'buildings_updated': 0,
            'rooms_created': 0,
            'rooms_updated': 0,
            'employees_created': 0,
            'employees_updated': 0,
            'residences_created': 0,
            'residences_updated': 0,
            'residences_skipped': 0,
            'errors': []
        }
        
        headers = ws.row_values(0)
        print(f"\n表头: {headers}")
        print(f"\n总行数: {ws.nrows - 1}")
        print("\n开始处理数据...\n")
        
        for row_idx in range(1, ws.nrows):
            row = ws.row_values(row_idx)
            
            try:
                # 解析数据
                building_raw = row[0] if len(row) > 0 else None
                room_raw = row[1] if len(row) > 1 else None
                room_unit = str(int(row[2])) if len(row) > 2 and row[2] else None
                room_name = str(row[3]).strip() if len(row) > 3 else None
                company = str(row[4]).strip() if len(row) > 4 and row[4] else None
                department = str(row[5]).strip() if len(row) > 5 and row[5] else None
                position = str(row[6]).strip() if len(row) > 6 and row[6] else None
                name = str(row[7]).strip() if len(row) > 7 else None
                remark = str(row[8]).strip() if len(row) > 8 and row[8] else None
                
                if not building_raw or not room_raw or not name:
                    stats['errors'].append(f"第{row_idx + 1}行: 楼栋/房号/姓名为空")
                    continue
                
                building_no, room_no = parse_building_and_room(building_raw, room_raw)
                
                # 1. 处理楼栋
                cache_key = building_no
                if cache_key not in building_cache:
                    building = db.query(Building).filter(
                        and_(
                            Building.building_no == building_no,
                            Building.deleted_at.is_(None)
                        )
                    ).first()
                    
                    if not building:
                        building = Building(
                            building_no=building_no,
                            name=f"{building_no}栋",
                            status='active'
                        )
                        db.add(building)
                        db.flush()
                        stats['buildings_created'] += 1
                        print(f"✓ 创建楼栋: {building_no}")
                    else:
                        stats['buildings_updated'] += 1
                    
                    building_cache[cache_key] = building.id
                
                building_id = building_cache[cache_key]
                
                # 2. 处理房间
                room_cache_key = f"{building_no}-{room_no}-{room_unit}"
                if room_cache_key not in room_cache:
                    room = db.query(Room).filter(
                        and_(
                            Room.building_id == building_id,
                            Room.room_no == room_no,
                            Room.room_unit == room_unit,
                            Room.deleted_at.is_(None)
                        )
                    ).first()
                    
                    if not room:
                        room = Room(
                            building_id=building_id,
                            room_no=room_no,
                            room_unit=room_unit,
                            room_name=room_name or f"{room_no}-{room_unit}",
                            electricity_price=0.49,
                            water_unit_price=3.5,
                            rent_standard=0
                        )
                        db.add(room)
                        db.flush()
                        stats['rooms_created'] += 1
                        print(f"✓ 创建房间: {building_no}-{room_no}-{room_unit} ({room_name})")
                    else:
                        # 更新房间名称
                        if room_name and room.room_name != room_name:
                            room.room_name = room_name
                        stats['rooms_updated'] += 1
                    
                    room_cache[room_cache_key] = room.id
                
                room_id = room_cache[room_cache_key]
                
                # 3. 处理员工
                if name not in employee_cache:
                    employee = db.query(Employee).filter(
                        and_(
                            Employee.name == name,
                            Employee.deleted_at.is_(None)
                        )
                    ).first()
                    
                    if not employee:
                        # 生成工号（如果没有）
                        employee_no = name  # 暂时用姓名作为工号
                        employee = Employee(
                            employee_no=employee_no,
                            name=name,
                            company=company,
                            department=department,
                            position=position,
                            status='active'
                        )
                        db.add(employee)
                        db.flush()
                        stats['employees_created'] += 1
                        print(f"✓ 创建员工: {name} ({company or ''}/{department or ''})")
                    else:
                        # 更新员工信息
                        if company and employee.company != company:
                            employee.company = company
                        if department and employee.department != department:
                            employee.department = department
                        if position and employee.position != position:
                            employee.position = position
                        stats['employees_updated'] += 1
                    
                    employee_cache[name] = employee.id
                
                employee_id = employee_cache[name]
                
                # 4. 处理入住记录
                # 检查是否已有有效入住记录
                existing = db.query(ResidenceRecord).filter(
                    and_(
                        ResidenceRecord.employee_id == employee_id,
                        ResidenceRecord.room_id == room_id,
                        ResidenceRecord.check_out_date.is_(None)
                    )
                ).first()
                
                # 判断是否为主缴费人（检测"夫妻间"关键词）
                is_primary = 1 if remark and '夫妻间' in remark else 0
                
                if existing:
                    if mode == 'add_only':
                        stats['residences_skipped'] += 1
                        continue
                    # 更新入住记录
                    if remark and existing.remark != remark:
                        existing.remark = remark
                    if existing.is_primary_payer != is_primary:
                        existing.is_primary_payer = is_primary
                    stats['residences_updated'] += 1
                else:
                    # 创建新入住记录
                    residence = ResidenceRecord(
                        employee_id=employee_id,
                        room_id=room_id,
                        check_in_date=date.today(),
                        is_primary_payer=is_primary,
                        status='valid',
                        remark=remark
                    )
                    db.add(residence)
                    stats['residences_created'] += 1
                    print(f"✓ 创建入住: {name} -> {building_no}-{room_no}-{room_unit}")
                
                # 每处理50行提交一次
                if row_idx % 50 == 0:
                    db.commit()
                    print(f"\n已处理 {row_idx}/{ws.nrows - 1} 行\n")
            
            except Exception as e:
                stats['errors'].append(f"第{row_idx + 1}行错误: {str(e)}")
                print(f"✗ 第{row_idx + 1}行错误: {str(e)}")
                continue
        
        # 最终提交
        db.commit()
        
        # 打印统计
        print("\n" + "=" * 80)
        print("导入完成！统计信息：")
        print("=" * 80)
        print(f"楼栋: 新建 {stats['buildings_created']}, 更新 {stats['buildings_updated']}")
        print(f"房间: 新建 {stats['rooms_created']}, 更新 {stats['rooms_updated']}")
        print(f"员工: 新建 {stats['employees_created']}, 更新 {stats['employees_updated']}")
        print(f"入住: 新建 {stats['residences_created']}, 更新 {stats['residences_updated']}, 跳过 {stats['residences_skipped']}")
        
        if stats['errors']:
            print(f"\n错误 {len(stats['errors'])} 条:")
            for err in stats['errors'][:10]:  # 只显示前10条
                print(f"  - {err}")
            if len(stats['errors']) > 10:
                print(f"  ... 还有 {len(stats['errors']) - 10} 条错误")
        
        return stats
    
    except Exception as e:
        db.rollback()
        print(f"\n导入失败: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import sys
    
    file_path = Path(__file__).parent.parent.parent / "data" / "房间和人员-最新.xls"
    
    # 从命令行参数获取模式
    mode = sys.argv[1] if len(sys.argv) > 1 else 'update'
    
    if mode not in ['update', 'override', 'add_only']:
        print("错误: 模式必须是 update, override 或 add_only")
        sys.exit(1)
    
    print(f"文件路径: {file_path}")
    print(f"导入模式: {mode}")
    print("\n确认导入？(y/n): ", end='')
    
    confirm = input().strip().lower()
    if confirm != 'y':
        print("已取消")
        sys.exit(0)
    
    import_personnel_data(file_path, mode)
