"""入住记录 API"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from ..database import get_db
from ..models import ResidenceRecord, Employee, Room, Building
from ..schemas.residence import (
    ResidenceCreate, ResidenceUpdate, ResidenceResponse, ResidenceListResponse,
    BatchMoveOut, BatchTransfer,
)
from ..utils.exceptions import NotFoundError, DuplicateError, BusinessError
from ..utils.date_utils import parse_date


router = APIRouter()


def _to_response_with_joins(res: ResidenceRecord, db: Session) -> ResidenceResponse:
    """转换为响应（带员工和房间信息）"""
    data = ResidenceResponse.model_validate(res)
    emp = db.query(Employee).filter(Employee.id == res.employee_id).first()
    room = db.query(Room).filter(Room.id == res.room_id).first()
    if emp:
        data.employee_name = emp.name
        data.employee_no = emp.employee_no
        data.company = emp.company
        data.department = emp.department
        data.position = emp.position
    if room:
        building = db.query(Building).filter(Building.id == room.building_id).first()
        data.room_no = room.room_no
        data.room_name = room.room_name
        data.building_id = room.building_id
        data.rent_standard = float(room.rent_standard) if room.rent_standard else 0
        data.electricity_price = float(room.electricity_price) if room.electricity_price else 0
        if building:
            data.building_no = building.building_no
            data.building_name = building.name
    return data


@router.get("", response_model=ResidenceListResponse)
def list_residences(
    building_id: Optional[int] = Query(None),
    room_id: Optional[int] = Query(None),
    building_no: Optional[str] = Query(None),
    room_no: Optional[str] = Query(None),
    keyword: Optional[str] = Query(None, description="姓名/工号搜索"),
    status: Optional[str] = Query(None, description="valid/invalid/business_trip/leave"),
    is_current: Optional[bool] = Query(None, description="仅看当前在住"),
    db: Session = Depends(get_db),
):
    """入住记录列表"""
    query = db.query(ResidenceRecord)
    if building_id:
        query = query.filter(ResidenceRecord.room_id.in_(
            db.query(Room.id).filter(Room.building_id == building_id)
        ))
    if room_id:
        query = query.filter(ResidenceRecord.room_id == room_id)
    if building_no:
        query = query.filter(ResidenceRecord.room_id.in_(
            db.query(Room.id).join(Building).filter(Building.building_no == building_no)
        ))
    if room_no:
        query = query.filter(ResidenceRecord.room_id.in_(
            db.query(Room.id).filter(Room.room_no == room_no)
        ))
    if status:
        query = query.filter(ResidenceRecord.status == status)
    if keyword:
        emp_ids = [
            e.id for e in db.query(Employee).filter(
                or_(Employee.name.like(f"%{keyword}%"), Employee.employee_no.like(f"%{keyword}%"))
            ).all()
        ]
        if emp_ids:
            query = query.filter(ResidenceRecord.employee_id.in_(emp_ids))
        else:
            query = query.filter(ResidenceRecord.id == -1)
    if is_current:
        from datetime import date
        today = date.today()
        query = query.filter(
            and_(
                ResidenceRecord.check_in_date <= today,
                or_(ResidenceRecord.check_out_date.is_(None), ResidenceRecord.check_out_date >= today),
            )
        )

    records = query.all()
    items = [_to_response_with_joins(r, db) for r in records]
    return {"items": items, "total": len(items)}


@router.post("", response_model=ResidenceResponse)
def create_residence(data: ResidenceCreate, db: Session = Depends(get_db)):
    """新增入住"""
    # 校验员工和房间存在
    emp = db.query(Employee).filter(
        and_(Employee.id == data.employee_id, Employee.deleted_at.is_(None))
    ).first()
    if not emp:
        raise NotFoundError(f"员工不存在: {data.employee_id}")
    room = db.query(Room).filter(
        and_(Room.id == data.room_id, Room.deleted_at.is_(None))
    ).first()
    if not room:
        raise NotFoundError(f"房间不存在: {data.room_id}")

    # 检查是否已有有效入住记录
    existing = db.query(ResidenceRecord).filter(
        and_(
            ResidenceRecord.employee_id == data.employee_id,
            ResidenceRecord.status != "invalid",
            ResidenceRecord.check_out_date.is_(None),
        )
    ).first()
    if existing:
        raise DuplicateError(f"员工已有有效入住记录(ID={existing.id})")

    res = ResidenceRecord(**data.model_dump())
    db.add(res)
    db.commit()
    db.refresh(res)
    return _to_response_with_joins(res, db)


@router.put("/{residence_id}", response_model=ResidenceResponse)
def update_residence(
    residence_id: int, data: ResidenceUpdate, db: Session = Depends(get_db),
):
    """编辑入住记录"""
    res = db.query(ResidenceRecord).filter(ResidenceRecord.id == residence_id).first()
    if not res:
        raise NotFoundError(f"入住记录不存在: {residence_id}")
    update_data = data.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(res, k, v)
    db.commit()
    db.refresh(res)
    return _to_response_with_joins(res, db)


@router.delete("/{residence_id}")
def delete_residence(residence_id: int, db: Session = Depends(get_db)):
    """删除入住记录"""
    res = db.query(ResidenceRecord).filter(ResidenceRecord.id == residence_id).first()
    if not res:
        raise NotFoundError(f"入住记录不存在: {residence_id}")
    db.delete(res)
    db.commit()
    return {"message": "ok"}


@router.post("/batch-move-out")
def batch_move_out(data: BatchMoveOut, db: Session = Depends(get_db)):
    """批量搬离"""
    move_date = parse_date(data.check_out_date)
    updated = 0
    for rid in data.residence_ids:
        res = db.query(ResidenceRecord).filter(ResidenceRecord.id == rid).first()
        if res and (res.check_out_date is None or res.check_out_date > move_date):
            res.check_out_date = move_date
            res.status = "invalid"
            updated += 1
    db.commit()
    return {"message": "ok", "updated": updated}


@router.post("/batch-transfer")
def batch_transfer(data: BatchTransfer, db: Session = Depends(get_db)):
    """批量换房"""
    transfer_date = parse_date(data.transfer_date)
    transferred = 0
    for item in data.items:
        old_res = db.query(ResidenceRecord).filter(
            ResidenceRecord.id == item.residence_id
        ).first()
        if not old_res:
            continue
        target_room = db.query(Room).filter(Room.id == item.target_room_id).first()
        if not target_room:
            continue
        # 旧记录搬离
        old_res.check_out_date = transfer_date
        old_res.status = "invalid"
        # 新记录入住
        new_res = ResidenceRecord(
            employee_id=old_res.employee_id,
            room_id=item.target_room_id,
            check_in_date=transfer_date,
            check_out_date=None,
            is_primary_payer=0,
            probation_months=0,
            status="valid",
            remark=old_res.remark,
        )
        db.add(new_res)
        transferred += 1
    db.commit()
    return {"message": "ok", "transferred": transferred}
