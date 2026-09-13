"""房号总电表服务"""
from decimal import Decimal
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import and_

from ..models import RoomMainMeterRecord, Room, Building
from ..utils.date_utils import prev_month_start


def get_or_create_room_main_meter(
    db: Session, building_id: int, room_no: str, target_month: date
) -> RoomMainMeterRecord:
    """获取或创建房号总电表记录，自动带出上月读数"""
    record = (
        db.query(RoomMainMeterRecord)
        .filter(
            and_(
                RoomMainMeterRecord.building_id == building_id,
                RoomMainMeterRecord.room_no == room_no,
                RoomMainMeterRecord.month == target_month,
            )
        )
        .first()
    )
    
    if record:
        return record
    
    # 查找上月记录
    prev_month = prev_month_start(target_month)
    prev_record = (
        db.query(RoomMainMeterRecord)
        .filter(
            and_(
                RoomMainMeterRecord.building_id == building_id,
                RoomMainMeterRecord.room_no == room_no,
                RoomMainMeterRecord.month == prev_month,
            )
        )
        .first()
    )
    
    # 从房间表获取电表编号（取该房号下任意一个房间的meter_no）
    sample_room = (
        db.query(Room)
        .filter(
            and_(
                Room.building_id == building_id,
                Room.room_no == room_no,
            )
        )
        .first()
    )
    meter_no = sample_room.meter_no if sample_room else None
    
    # 创建新记录
    previous_reading = prev_record.current_reading if prev_record else Decimal("0")
    record = RoomMainMeterRecord(
        building_id=building_id,
        room_no=room_no,
        month=target_month,
        meter_no=meter_no,
        previous_reading=previous_reading,
        current_reading=previous_reading,  # 初始值等于上月读数
        status="pending",
    )
    db.add(record)
    db.flush()
    return record


def update_room_main_meter(
    db: Session,
    building_id: int,
    room_no: str,
    target_month: date,
    previous_reading: Decimal | None = None,
    current_reading: Decimal | None = None,
    electricity_price: Decimal | None = None,
    meter_no: str | None = None,
    remark: str | None = None,
) -> RoomMainMeterRecord:
    """更新房号总电表读数并计算"""
    record = get_or_create_room_main_meter(db, building_id, room_no, target_month)
    
    if previous_reading is not None:
        record.previous_reading = previous_reading
    if current_reading is not None:
        record.current_reading = current_reading
    if electricity_price is not None:
        record.electricity_price = electricity_price
    if meter_no is not None:
        record.meter_no = meter_no
    if remark is not None:
        record.remark = remark
    
    # 计算用电量和费用
    record.total_degree = record.current_reading - record.previous_reading
    record.total_fee = record.total_degree * record.electricity_price
    
    # 更新状态
    if record.current_reading > record.previous_reading:
        record.status = "recorded"
    
    db.flush()
    return record


def calculate_room_main_meter_fee(
    db: Session, record: RoomMainMeterRecord
) -> RoomMainMeterRecord:
    """计算房号总电表费用"""
    record.total_degree = record.current_reading - record.previous_reading
    record.total_fee = record.total_degree * record.electricity_price
    record.status = "calculated"
    db.flush()
    return record


def init_all_room_main_meters_for_month(
    db: Session, target_month: date, building_id: int | None = None
) -> int:
    """初始化某月所有房号的总电表记录"""
    # 获取所有房号（去重）
    query = db.query(Room.building_id, Room.room_no).filter(Room.status == "active")
    if building_id:
        query = query.filter(Room.building_id == building_id)
    
    room_nos = query.distinct().all()
    
    count = 0
    for building_id, room_no in room_nos:
        try:
            get_or_create_room_main_meter(db, building_id, room_no, target_month)
            count += 1
        except Exception:
            pass
    
    db.flush()
    return count
