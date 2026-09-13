"""房号总电表服务"""
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models import RoomMainMeterRecord, MeterRecord, Room, Building
from ..schemas.room_main_meter import (
    RoomMainMeterCreate,
    RoomMainMeterUpdate,
    RoomMainMeterResponse,
    AcMeterUpdate,
    AcMeterResponse,
    CombinedMeterResponse,
)


class RoomMainMeterService:
    """房号总电表服务"""

    @staticmethod
    async def get_by_id(db: AsyncSession, record_id: int) -> Optional[RoomMainMeterRecord]:
        """根据ID获取记录"""
        result = await db.execute(
            select(RoomMainMeterRecord).where(RoomMainMeterRecord.id == record_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_room_month(
        db: AsyncSession,
        building_id: int,
        room_no: str,
        month: date
    ) -> Optional[RoomMainMeterRecord]:
        """根据楼栋、房号、月份获取记录"""
        result = await db.execute(
            select(RoomMainMeterRecord).where(
                and_(
                    RoomMainMeterRecord.building_id == building_id,
                    RoomMainMeterRecord.room_no == room_no,
                    RoomMainMeterRecord.month == month
                )
            )
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_combined_list(
        db: AsyncSession,
        month: date,
        building_id: Optional[int] = None
    ) -> list[CombinedMeterResponse]:
        """获取组合电表列表（总表+空调表）"""
        
        # 1. 获取所有房号总电表记录
        query = select(RoomMainMeterRecord, Building.building_no).join(
            Building, RoomMainMeterRecord.building_id == Building.id
        ).where(RoomMainMeterRecord.month == month)
        
        if building_id:
            query = query.where(RoomMainMeterRecord.building_id == building_id)
        
        query = query.order_by(Building.building_no, RoomMainMeterRecord.room_no)
        
        result = await db.execute(query)
        main_records = result.all()
        
        combined_list = []
        
        for main_record, building_no in main_records:
            # 2. 查询该房号下所有小房间的空调电表
            ac_query = select(MeterRecord, Room).join(
                Room, MeterRecord.room_id == Room.id
            ).where(
                and_(
                    Room.building_id == main_record.building_id,
                    Room.room_no == main_record.room_no,
                    MeterRecord.month == month
                )
            ).order_by(Room.room_name)
            
            ac_result = await db.execute(ac_query)
            ac_records = ac_result.all()
            
            # 3. 构建空调电表列表
            ac_meters = []
            total_ac_fee = Decimal("0")
            
            for ac_record, room in ac_records:
                # 获取入住人数
                occupants_count_query = select(func.count()).select_from(
                    select(1).where(
                        and_(
                            Room.id == room.id,
                            # 这里应该关联 ResidenceRecord 表，暂时返回0
                        )
                    ).subquery()
                )
                # occupants_count = (await db.execute(occupants_count_query)).scalar() or 0
                occupants_count = 0  # 简化处理
                
                ac_meter = AcMeterResponse(
                    id=ac_record.id,
                    room_id=ac_record.room_id,
                    month=ac_record.month,
                    ac_previous_reading=ac_record.ac_previous_reading or Decimal("0"),
                    ac_current_reading=ac_record.ac_current_reading or Decimal("0"),
                    ac_degree=ac_record.ac_degree or Decimal("0"),
                    ac_unit_price=ac_record.ac_unit_price or Decimal("0"),
                    ac_fee=ac_record.ac_fee or Decimal("0"),
                    status=ac_record.status,
                    remark=ac_record.remark,
                    created_at=ac_record.created_at,
                    building_no=building_no,
                    room_no=room.room_no,
                    room_name=room.room_name,
                    ac_meter_no=room.ac_meter_no,
                    occupants_count=occupants_count
                )
                ac_meters.append(ac_meter)
                total_ac_fee += ac_meter.ac_fee
            
            # 4. 构建组合响应
            combined = CombinedMeterResponse(
                building_id=main_record.building_id,
                building_no=building_no,
                room_no=main_record.room_no,
                month=main_record.month,
                main_meter_id=main_record.id,
                main_meter_no=main_record.meter_no,
                main_previous_reading=main_record.previous_reading,
                main_current_reading=main_record.current_reading,
                main_total_degree=main_record.total_degree,
                main_electricity_price=main_record.electricity_price,
                main_total_fee=main_record.total_fee,
                main_status=main_record.status,
                ac_meters=ac_meters,
                total_ac_fee=total_ac_fee,
                grand_total=main_record.total_fee + total_ac_fee
            )
            combined_list.append(combined)
        
        return combined_list

    @staticmethod
    async def init_month_main_meters(
        db: AsyncSession,
        month: date,
        building_id: Optional[int] = None
    ) -> int:
        """初始化月度房号总电表（自动带出上月读数）"""
        
        # 1. 获取所有需要初始化的房号（从rooms表去重）
        query = select(Room.building_id, Room.room_no).distinct()
        if building_id:
            query = query.where(Room.building_id == building_id)
        
        result = await db.execute(query)
        rooms = result.all()
        
        count = 0
        prev_month = date(month.year, month.month - 1, 1) if month.month > 1 else date(month.year - 1, 12, 1)
        
        for building_id_val, room_no in rooms:
            # 检查是否已存在
            existing = await RoomMainMeterService.get_by_room_month(
                db, building_id_val, room_no, month
            )
            if existing:
                continue
            
            # 获取上月记录
            prev_record = await RoomMainMeterService.get_by_room_month(
                db, building_id_val, room_no, prev_month
            )
            
            previous_reading = prev_record.current_reading if prev_record else Decimal("0")
            
            # 创建新记录
            new_record = RoomMainMeterRecord(
                building_id=building_id_val,
                room_no=room_no,
                month=month,
                previous_reading=previous_reading,
                current_reading=previous_reading,  # 初始值等于上月
                total_degree=Decimal("0"),
                electricity_price=Decimal("0.4900"),
                total_fee=Decimal("0"),
                status="pending"
            )
            db.add(new_record)
            count += 1
        
        await db.commit()
        return count

    @staticmethod
    async def update_main_meter(
        db: AsyncSession,
        building_id: int,
        room_no: str,
        month: date,
        data: RoomMainMeterUpdate
    ) -> RoomMainMeterRecord:
        """更新房号总电表读数"""
        
        record = await RoomMainMeterService.get_by_room_month(db, building_id, room_no, month)
        if not record:
            raise ValueError(f"记录不存在: {building_id}-{room_no}-{month}")
        
        # 更新字段
        if data.previous_reading is not None:
            record.previous_reading = data.previous_reading
        if data.current_reading is not None:
            record.current_reading = data.current_reading
        if data.electricity_price is not None:
            record.electricity_price = data.electricity_price
        if data.meter_no is not None:
            record.meter_no = data.meter_no
        if data.remark is not None:
            record.remark = data.remark
        
        # 计算用电量和费用
        record.total_degree = record.current_reading - record.previous_reading
        record.total_fee = record.total_degree * record.electricity_price
        record.status = "recorded" if record.current_reading > record.previous_reading else "pending"
        record.updated_at = datetime.now()
        
        await db.commit()
        await db.refresh(record)
        return record

    @staticmethod
    async def update_ac_meter(
        db: AsyncSession,
        room_id: int,
        month: date,
        data: AcMeterUpdate
    ) -> MeterRecord:
        """更新空调电表读数"""
        
        # 查询meter_records表
        result = await db.execute(
            select(MeterRecord).where(
                and_(
                    MeterRecord.room_id == room_id,
                    MeterRecord.month == month
                )
            )
        )
        record = result.scalar_one_or_none()
        if not record:
            raise ValueError(f"空调电表记录不存在: room_id={room_id}, month={month}")
        
        # 更新字段
        if data.ac_previous_reading is not None:
            record.ac_previous_reading = data.ac_previous_reading
        if data.ac_current_reading is not None:
            record.ac_current_reading = data.ac_current_reading
        if data.ac_unit_price is not None:
            record.ac_unit_price = data.ac_unit_price
        if data.remark is not None:
            record.remark = data.remark
        
        # 计算用电量和费用
        record.ac_degree = record.ac_current_reading - record.ac_previous_reading
        record.ac_fee = record.ac_degree * record.ac_unit_price
        record.status = "recorded" if record.ac_current_reading > record.ac_previous_reading else "pending"
        record.updated_at = datetime.now()
        
        await db.commit()
        await db.refresh(record)
        return record
