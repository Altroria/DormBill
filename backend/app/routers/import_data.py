"""Excel 导入 API"""
from io import BytesIO
from fastapi import APIRouter, Depends, UploadFile, File, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import date
import xlrd
import tempfile
import os

from ..database import get_db
from ..models import Employee, Room, Building, ResidenceRecord
from ..services.excel_service import (
    import_employees_from_excel, import_rooms_from_excel,
    import_residences_from_excel,
)
from ..utils.exceptions import ValidationError


router = APIRouter()


@router.post("/employees")
async def import_employees(
    file: UploadFile = File(...), db: Session = Depends(get_db),
):
    """导入员工 Excel"""
    content = await file.read()
    bio = BytesIO(content)
    result = import_employees_from_excel(bio)
    created = 0
    for row in result["rows"]:
        existing = db.query(Employee).filter(
            and_(
                Employee.employee_no == row["employee_no"],
                Employee.deleted_at.is_(None),
            )
        ).first()
        if existing:
            continue
        emp = Employee(**row)
        db.add(emp)
        created += 1
    db.commit()
    return {
        "message": "ok",
        "total": len(result["rows"]),
        "created": created,
        "errors": result.get("errors", []),
    }


@router.post("/rooms")
async def import_rooms(
    file: UploadFile = File(...), db: Session = Depends(get_db),
):
    """导入房间 Excel"""
    content = await file.read()
    bio = BytesIO(content)
    result = import_rooms_from_excel(bio)
    building_cache = {}
    created = 0
    for row in result["rows"]:
        bno = row.pop("building_no")
        # 楼栋：不存在则创建
        if bno not in building_cache:
            b = db.query(Building).filter(
                and_(Building.building_no == bno, Building.deleted_at.is_(None))
            ).first()
            if not b:
                b = Building(building_no=bno, name=f"{bno}栋", status="active")
                db.add(b)
                db.flush()
            building_cache[bno] = b.id
        building_id = building_cache[bno]

        existing = db.query(Room).filter(
            and_(
                Room.building_id == building_id,
                Room.room_no == row["room_no"],
                Room.room_name == row["room_name"],
                Room.deleted_at.is_(None),
            )
        ).first()
        if existing:
            continue
        room = Room(building_id=building_id, **row)
        db.add(room)
        created += 1
    db.commit()
    return {
        "message": "ok",
        "total": len(result["rows"]),
        "created": created,
        "errors": result.get("errors", []),
    }


@router.post("/residences")
async def import_residences(
    file: UploadFile = File(...), db: Session = Depends(get_db),
):
    """批量导入入住记录"""
    content = await file.read()
    bio = BytesIO(content)
    result = import_residences_from_excel(bio)
    created = 0
    for row in result["rows"]:
        # 检查重复
        existing = db.query(ResidenceRecord).filter(
            and_(
                ResidenceRecord.employee_id == row["employee_id"],
                ResidenceRecord.status != "invalid",
                ResidenceRecord.check_out_date.is_(None),
            )
        ).first()
        if existing:
            continue
        res = ResidenceRecord(**row)
        db.add(res)
        created += 1
    db.commit()
    return {
        "message": "ok",
        "total": len(result["rows"]),
        "created": created,
        "errors": result.get("errors", []),
    }


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


@router.post("/personnel")
async def import_personnel_data(
    file: UploadFile = File(...),
    mode: str = Query("update", pattern="^(update|override|add_only)$"),
    db: Session = Depends(get_db),
):
    """
    导入房间和人员综合数据（从Excel一次性导入楼栋、房间、员工、入住信息）
    
    mode参数:
    - update: 更新模式（默认），已存在则更新，不存在则创建
    - override: 覆盖模式，先清空所有入住记录，再重新导入
    - add_only: 仅添加模式，跳过已存在的记录
    
    Excel格式要求:
    第1行为表头，包含: 楼号 | 房号 | 室号 | 房间 | 任职单位 | 一级部门 | 职务 | 姓名 | 转宿日期，备注
    """
    # 保存上传的文件到临时位置
    content = await file.read()
    
    # 写入临时文件
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xls') as tmp:
        tmp.write(content)
        tmp_path = tmp.name
    
    try:
        # 读取Excel
        wb = xlrd.open_workbook(tmp_path)
        ws = wb.sheet_by_index(0)
        
        # 如果是覆盖模式，先清空入住记录
        if mode == 'override':
            deleted_count = db.query(ResidenceRecord).delete()
            db.commit()
        
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
        
        # 跳过表头（第0行）
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
                    stats['errors'].append({"row": row_idx + 1, "msg": "楼栋/房号/姓名为空"})
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
                existing = db.query(ResidenceRecord).filter(
                    and_(
                        ResidenceRecord.employee_id == employee_id,
                        ResidenceRecord.room_id == room_id,
                        ResidenceRecord.check_out_date.is_(None)
                    )
                ).first()
                
                # 判断是否为主缴费人
                # 默认所有人都是主缴费人(1)，只有备注明确标注"配偶"或"夫妻间副"才设为非主缴费人(0)
                is_primary = 0 if remark and ('配偶' in remark or '夫妻间副' in remark) else 1
                
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
                
                # 每处理50行提交一次
                if row_idx % 50 == 0:
                    db.commit()
            
            except Exception as e:
                stats['errors'].append({"row": row_idx + 1, "msg": str(e)})
                continue
        
        # 最终提交
        db.commit()
        
        return {
            "message": "ok",
            "mode": mode,
            "stats": stats
        }
    
    except Exception as e:
        db.rollback()
        raise ValidationError(f"导入失败: {str(e)}")
    finally:
        # 删除临时文件
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
