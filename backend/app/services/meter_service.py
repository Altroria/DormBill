"""电表服务：上月读数查询、用量计算、异常检查"""
from decimal import Decimal
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import and_

from ..models import MeterRecord, Room
from ..utils.date_utils import add_months, month_start
from ..utils.decimal_utils import to_decimal, round_money, round_degree


def get_previous_reading(db: Session, room_id: int, current_month: date) -> Decimal:
    """获取上月的电表读数（普通+空调）"""
    prev_month = add_months(month_start(current_month), -1)
    record = db.query(MeterRecord).filter(
        and_(
            MeterRecord.room_id == room_id,
            MeterRecord.month == prev_month,
        )
    ).first()
    if record:
        return to_decimal(record.current_reading)
    return Decimal("0")


def get_previous_ac_reading(db: Session, room_id: int, current_month: date) -> Decimal:
    """获取上月的空调电表读数"""
    prev_month = add_months(month_start(current_month), -1)
    record = db.query(MeterRecord).filter(
        and_(
            MeterRecord.room_id == room_id,
            MeterRecord.month == prev_month,
        )
    ).first()
    if record:
        return to_decimal(record.ac_current_reading)
    return Decimal("0")


def is_meter_abnormal(previous: Decimal, current: Decimal) -> bool:
    """电表异常检查：当前读数 < 上月读数"""
    return current < previous


def calculate_degree(previous: Decimal, current: Decimal) -> Decimal:
    """计算用电量（普通）"""
    return round_degree(current - previous)


def calculate_ac_degree(previous: Decimal, current: Decimal) -> Decimal:
    """计算空调用电量"""
    return round_degree(current - previous)


def get_or_create_meter_record(
    db: Session,
    room_id: int,
    target_month: date,
) -> MeterRecord:
    """获取或创建电表记录（不存在则创建空记录）"""
    target_month = month_start(target_month)
    record = db.query(MeterRecord).filter(
        and_(
            MeterRecord.room_id == room_id,
            MeterRecord.month == target_month,
        )
    ).first()

    if record:
        return record

    # 新建空记录，自动带出上月读数
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise ValueError(f"房间不存在: {room_id}")

    prev_reading = get_previous_reading(db, room_id, target_month)
    prev_ac_reading = get_previous_ac_reading(db, room_id, target_month)

    record = MeterRecord(
        room_id=room_id,
        month=target_month,
        previous_reading=prev_reading,
        current_reading=Decimal("0"),
        total_degree=Decimal("0"),
        ac_previous_reading=prev_ac_reading,
        ac_current_reading=Decimal("0"),
        ac_degree=Decimal("0"),
        electricity_price=to_decimal(room.electricity_price),
        ac_unit_price=Decimal("0"),
        total_fee=Decimal("0"),
        ac_fee=Decimal("0"),
        status="normal",
    )
    db.add(record)
    db.flush()
    return record


def update_meter_readings(
    db: Session,
    room_id: int,
    target_month: date,
    current_reading: Decimal | None = None,
    ac_current_reading: Decimal | None = None,
    electricity_price: Decimal | None = None,
    ac_unit_price: Decimal | None = None,
    remark: str | None = None,
) -> MeterRecord:
    """更新电表读数"""
    record = get_or_create_meter_record(db, room_id, target_month)

    abnormal = False

    if current_reading is not None:
        record.current_reading = current_reading
        prev = to_decimal(record.previous_reading)
        if is_meter_abnormal(prev, current_reading):
            abnormal = True
        else:
            record.total_degree = calculate_degree(prev, current_reading)
            record.total_fee = round_money(record.total_degree * to_decimal(record.electricity_price))

    if ac_current_reading is not None:
        record.ac_current_reading = ac_current_reading
        prev = to_decimal(record.ac_previous_reading)
        if is_meter_abnormal(prev, ac_current_reading):
            abnormal = True
        else:
            record.ac_degree = calculate_ac_degree(prev, ac_current_reading)
            if to_decimal(record.ac_unit_price) > 0:
                record.ac_fee = round_money(record.ac_degree * to_decimal(record.ac_unit_price))

    if electricity_price is not None:
        record.electricity_price = electricity_price
        if to_decimal(record.total_degree) > 0:
            record.total_fee = round_money(record.total_degree * electricity_price)

    if ac_unit_price is not None:
        record.ac_unit_price = ac_unit_price
        if to_decimal(record.ac_degree) > 0:
            record.ac_fee = round_money(record.ac_degree * ac_unit_price)

    if remark is not None:
        record.remark = remark

    if abnormal:
        record.status = "abnormal"

    db.flush()
    return record


__all__ = [
    "get_previous_reading",
    "get_previous_ac_reading",
    "is_meter_abnormal",
    "calculate_degree",
    "calculate_ac_degree",
    "get_or_create_meter_record",
    "update_meter_readings",
]
