"""电表 API"""
from typing import Optional
from decimal import Decimal
from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_

from ..database import get_db
from ..models import MeterRecord, Room, Building
from ..schemas.meter import (
    MeterCreate, MeterUpdate, MeterResponse, MeterListResponse,
    MeterCalculateRequest,
)
from ..services.meter_service import (
    update_meter_readings, get_or_create_meter_record,
)
from ..services.electricity_service import (
    get_valid_occupants_for_room, calculate_all_electricity_for_month,
)
from ..utils.exceptions import NotFoundError
from ..utils.date_utils import parse_date, month_start


router = APIRouter()


def _to_response(m: MeterRecord, room: Room | None, building: Building | None,
                 occupants_count: int = 0) -> MeterResponse:
    data = MeterResponse.model_validate(m)
    if room:
        data.room_no = room.room_no
        data.room_name = room.room_name
        data.meter_no = room.meter_no
        data.ac_meter_no = room.ac_meter_no
        data.occupants_count = occupants_count
    if building:
        data.building_no = building.building_no
    return data


@router.get("", response_model=MeterListResponse)
def list_meters(
    month: str = Query(..., description="YYYY-MM"),
    building_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    """电表记录列表（按月份）"""
    target_month = month_start(parse_date(month + "-01"))
    query = (
        db.query(MeterRecord, Room, Building)
        .join(Room, MeterRecord.room_id == Room.id)
        .join(Building, Room.building_id == Building.id)
        .filter(MeterRecord.month == target_month)
    )
    if building_id:
        query = query.filter(Room.building_id == building_id)
    rows = query.order_by(
        Building.building_no, Room.room_no, Room.room_name
    ).all()
    items = []
    for m, room, building in rows:
        occupants = get_valid_occupants_for_room(db, room.id, target_month)
        items.append(_to_response(m, room, building, len(occupants)))
    return {"items": items, "total": len(items)}


@router.put("/{room_id}/{month}", response_model=MeterResponse)
def update_meter(
    room_id: int,
    month: str,
    data: MeterUpdate,
    db: Session = Depends(get_db),
):
    """更新电表读数"""
    target_month = month_start(parse_date(month + "-01"))
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise NotFoundError(f"房间不存在: {room_id}")
    building = db.query(Building).filter(Building.id == room.building_id).first()

    record = update_meter_readings(
        db,
        room_id=room_id,
        target_month=target_month,
        previous_reading=data.previous_reading,
        current_reading=data.current_reading,
        ac_previous_reading=data.ac_previous_reading,
        ac_current_reading=data.ac_current_reading,
        electricity_price=data.electricity_price,
        ac_unit_price=data.ac_unit_price,
        remark=data.remark,
    )
    db.commit()
    db.refresh(record)
    occupants = get_valid_occupants_for_room(db, room_id, target_month)
    return _to_response(record, room, building, len(occupants))


@router.post("/calculate")
def calculate_meters(
    data: MeterCalculateRequest, db: Session = Depends(get_db),
):
    """批量计算电费（按月）"""
    target_month = month_start(parse_date(data.month))
    count = calculate_all_electricity_for_month(
        db, target_month, data.ac_unit_price,
    )
    db.commit()
    return {"message": "ok", "count": count}


@router.post("/init-month")
def init_meter_records(
    month: str,
    building_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    """初始化某月的电表记录（带出上月读数）"""
    target_month = month_start(parse_date(month + "-01"))
    query = db.query(Room).filter(Room.status == "active")
    if building_id:
        query = query.filter(Room.building_id == building_id)
    rooms = query.all()
    count = 0
    for room in rooms:
        try:
            get_or_create_meter_record(db, room.id, target_month)
            count += 1
        except Exception:
            pass
    db.commit()
    return {"message": "ok", "count": count}
