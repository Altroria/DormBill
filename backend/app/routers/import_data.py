"""Excel 导入 API"""
from io import BytesIO
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import and_

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
