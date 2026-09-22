"""水表记录服务"""
from decimal import Decimal
from datetime import date
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from ..models import WaterMeterRecord, Room, ResidenceRecord, Employee
from ..utils.date_utils import month_start, month_end, stay_days_in_month
from ..utils.decimal_utils import to_decimal, round_money


def init_water_meters_for_month(
    db: Session,
    target_month: date,
    building_id: Optional[int] = None,
) -> List[WaterMeterRecord]:
    """
    初始化某月的水表记录
    
    为每个活跃房间创建一条空记录，自动继承上月读数
    """
    target_month = month_start(target_month)
    
    # 查询房间
    query = db.query(Room).filter(Room.status == "active")
    if building_id:
        query = query.filter(Room.building_id == building_id)
    rooms = query.all()
    
    # 上月
    from dateutil.relativedelta import relativedelta
    prev_month = target_month - relativedelta(months=1)
    
    created = []
    for room in rooms:
        # 检查是否已存在
        existing = db.query(WaterMeterRecord).filter(
            and_(
                WaterMeterRecord.room_no == room.room_no,
                WaterMeterRecord.month == target_month,
            )
        ).first()
        
        if existing:
            continue
        
        # 查询上月读数
        prev_record = db.query(WaterMeterRecord).filter(
            and_(
                WaterMeterRecord.room_no == room.room_no,
                WaterMeterRecord.month == prev_month,
            )
        ).first()
        
        previous_reading = Decimal("0")
        if prev_record and prev_record.current_reading:
            previous_reading = prev_record.current_reading
        
        record = WaterMeterRecord(
            room_no=room.room_no,
            building_id=room.building_id,
            month=target_month,
            water_meter_no=room.water_meter_no,
            previous_reading=previous_reading,
            current_reading=Decimal("0"),
            usage=Decimal("0"),
            unit_price=Decimal("3.5"),  # 默认单价
            total_fee=Decimal("0"),
            status="normal",
        )
        db.add(record)
        created.append(record)
    
    db.flush()
    return created


def update_water_meter(
    db: Session,
    record_id: int,
    previous_reading: Optional[Decimal] = None,
    current_reading: Optional[Decimal] = None,
    unit_price: Optional[Decimal] = None,
    remark: Optional[str] = None,
) -> WaterMeterRecord:
    """
    更新水表记录并自动计算
    """
    record = db.query(WaterMeterRecord).filter(
        WaterMeterRecord.id == record_id
    ).first()
    
    if not record:
        raise ValueError("水表记录不存在")
    
    # 更新字段
    if previous_reading is not None:
        record.previous_reading = to_decimal(previous_reading)
    if current_reading is not None:
        record.current_reading = to_decimal(current_reading)
    if unit_price is not None:
        record.unit_price = to_decimal(unit_price)
    if remark is not None:
        record.remark = remark
    
    # 自动计算
    prev = to_decimal(record.previous_reading)
    curr = to_decimal(record.current_reading)
    price = to_decimal(record.unit_price)
    
    usage = curr - prev
    record.usage = usage
    record.total_fee = round_money(usage * price)
    
    # 异常检测
    if curr < prev:
        record.status = "abnormal"
    elif record.status == "abnormal":
        record.status = "normal"
    
    db.flush()
    return record


def get_employee_water_fee_for_month(
    db: Session,
    employee_id: int,
    target_month: date,
) -> Decimal:
    """
    获取员工某月的水费
    
    逻辑：
    1. 查询该员工当月的有效入住记录
    2. 获取对应房间的水表记录
    3. 按入住人数平分
    """
    target_month = month_start(target_month)
    
    # 查询员工当月入住记录
    residence = db.query(ResidenceRecord).filter(
        and_(
            ResidenceRecord.employee_id == employee_id,
            ResidenceRecord.status != "invalid",
        )
    ).first()
    
    if not residence:
        return Decimal("0")
    
    # 检查当月是否有效
    days = stay_days_in_month(
        residence.check_in_date,
        residence.check_out_date,
        target_month,
    )
    if days <= 0:
        return Decimal("0")
    
    # 查询房间水表记录 - 使用 room_no 而不是 room_id
    room = db.query(Room).filter(Room.id == residence.room_id).first()
    if not room:
        return Decimal("0")
    
    water_record = db.query(WaterMeterRecord).filter(
        and_(
            WaterMeterRecord.room_no == room.room_no,
            WaterMeterRecord.month == target_month,
        )
    ).first()
    
    if not water_record or not water_record.total_fee:
        return Decimal("0")
    
    # 查询该房间当月所有有效入住人数
    all_residences = db.query(ResidenceRecord).filter(
        and_(
            ResidenceRecord.room_id == residence.room_id,
            ResidenceRecord.status != "invalid",
        )
    ).all()
    
    # 统计有效人数（当月住满15天以上）
    valid_count = 0
    for res in all_residences:
        res_days = stay_days_in_month(res.check_in_date, res.check_out_date, target_month)
        if res_days > 15:  # 半月规则
            # 排除出差等特殊情况
            if res.remark and "出差" in res.remark:
                continue
            # 排除非主缴费人（夫妻同住只收一人）
            if not res.is_primary_payer:
                continue
            valid_count += 1
    
    if valid_count == 0:
        return Decimal("0")
    
    # 平均分摊
    total_fee = to_decimal(water_record.total_fee)
    per_person_fee = round_money(total_fee / valid_count)
    
    return per_person_fee


def batch_update_water_meters(
    db: Session,
    updates: List[Dict],
) -> List[WaterMeterRecord]:
    """
    批量更新水表记录
    
    updates: [{"room_no": "201", "month": "2024-10-01", "current_reading": 123.45, ...}]
    """
    updated = []
    for item in updates:
        room_no = item.get("room_no")
        month = month_start(item.get("month"))
        
        record = db.query(WaterMeterRecord).filter(
            and_(
                WaterMeterRecord.room_no == room_no,
                WaterMeterRecord.month == month,
            )
        ).first()
        
        if not record:
            continue
        
        record = update_water_meter(
            db,
            record.id,
            previous_reading=item.get("previous_reading"),
            current_reading=item.get("current_reading"),
            unit_price=item.get("unit_price"),
            remark=item.get("remark"),
        )
        updated.append(record)
    
    db.flush()
    return updated


__all__ = [
    "init_water_meters_for_month",
    "update_water_meter",
    "get_employee_water_fee_for_month",
    "batch_update_water_meters",
]
