"""房间 API"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from ..database import get_db
from ..models import Room, Building
from ..schemas.room import (
    RoomCreate, RoomUpdate, RoomResponse, RoomListResponse, RoomBatchCreate,
)
from ..utils.exceptions import NotFoundError, DuplicateError


router = APIRouter()


def _to_response(room: Room, building: Building | None) -> RoomResponse:
    """转换为响应对象（附带楼栋信息）"""
    data = RoomResponse.model_validate(room)
    if building:
        data.building_no = building.building_no
        data.building_name = building.name
    return data


@router.get("", response_model=RoomListResponse)
def list_rooms(
    building_id: Optional[int] = Query(None, description="楼栋ID"),
    keyword: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """房间列表"""
    query = db.query(Room, Building).join(
        Building, Room.building_id == Building.id
    ).filter(Room.deleted_at.is_(None))
    if building_id:
        query = query.filter(Room.building_id == building_id)
    if keyword:
        kw = f"%{keyword}%"
        query = query.filter(
            or_(Room.room_no.like(kw), Room.room_name.like(kw))
        )
    if status:
        query = query.filter(Room.status == status)
    query = query.order_by(
        Building.building_no.asc(), Room.room_no.asc(), Room.room_name.asc(),
    )
    rows = query.all()
    items = [_to_response(r, b) for r, b in rows]
    return {"items": items, "total": len(items)}


@router.post("", response_model=RoomResponse)
def create_room(data: RoomCreate, db: Session = Depends(get_db)):
    """新增房间"""
    existing = db.query(Room).filter(
        and_(
            Room.building_id == data.building_id,
            Room.room_no == data.room_no,
            Room.room_name == data.room_name,
            Room.deleted_at.is_(None),
        )
    ).first()
    if existing:
        raise DuplicateError(
            f"该楼栋下房号+房间名已存在: {data.room_no}-{data.room_name}"
        )
    building = db.query(Building).filter(Building.id == data.building_id).first()
    if not building:
        raise NotFoundError(f"楼栋不存在: {data.building_id}")
    room = Room(**data.model_dump())
    db.add(room)
    db.commit()
    db.refresh(room)
    return _to_response(room, building)


@router.post("/batch", response_model=RoomListResponse)
def batch_create_rooms(data: RoomBatchCreate, db: Session = Depends(get_db)):
    """批量新增房间"""
    building = db.query(Building).filter(Building.id == data.building_id).first()
    if not building:
        raise NotFoundError(f"楼栋不存在: {data.building_id}")

    created = []
    for item in data.items:
        item_dict = item.model_dump()
        item_dict["building_id"] = data.building_id
        existing = db.query(Room).filter(
            and_(
                Room.building_id == data.building_id,
                Room.room_no == item.room_no,
                Room.room_name == item.room_name,
                Room.deleted_at.is_(None),
            )
        ).first()
        if existing:
            continue
        room = Room(**item_dict)
        db.add(room)
        created.append(room)
    db.commit()
    for r in created:
        db.refresh(r)
    items = [_to_response(r, building) for r in created]
    return {"items": items, "total": len(items)}


@router.get("/{room_id}", response_model=RoomResponse)
def get_room(room_id: int, db: Session = Depends(get_db)):
    """房间详情"""
    row = db.query(Room, Building).join(
        Building, Room.building_id == Building.id
    ).filter(and_(Room.id == room_id, Room.deleted_at.is_(None))).first()
    if not row:
        raise NotFoundError(f"房间不存在: {room_id}")
    room, building = row
    return _to_response(room, building)


@router.put("/{room_id}", response_model=RoomResponse)
def update_room(room_id: int, data: RoomUpdate, db: Session = Depends(get_db)):
    """编辑房间"""
    row = db.query(Room, Building).join(
        Building, Room.building_id == Building.id
    ).filter(and_(Room.id == room_id, Room.deleted_at.is_(None))).first()
    if not row:
        raise NotFoundError(f"房间不存在: {room_id}")
    room, building = row
    update_data = data.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(room, k, v)
    db.commit()
    db.refresh(room)
    return _to_response(room, building)


@router.delete("/{room_id}")
def delete_room(room_id: int, db: Session = Depends(get_db)):
    """删除房间（软删除）"""
    room = db.query(Room).filter(
        and_(Room.id == room_id, Room.deleted_at.is_(None))
    ).first()
    if not room:
        raise NotFoundError(f"房间不存在: {room_id}")
    room.deleted_at = room.updated_at
    db.commit()
    return {"message": "ok"}
