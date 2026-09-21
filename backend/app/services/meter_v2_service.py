"""电表管理V2服务（同步版本）- 总表+空调表分离"""
from decimal import Decimal
from datetime import date
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, or_

from ..models.meter import MeterRecord
from ..models.room_main_meter import RoomMainMeterRecord
from ..models.room import Room
from ..models.building import Building
from ..models.residence import ResidenceRecord


class MeterV2Service:
    """电表V2服务 - 同步版本"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def init_month(
        self,
        month: date,
        building_id: Optional[int] = None,
    ) -> Dict[str, int]:
        """初始化月度电表记录（总表+空调表）"""
        # 查询房间列表
        rooms_query = self.db.query(Room)
        if building_id:
            rooms_query = rooms_query.filter(Room.building_id == building_id)
        
        rooms = rooms_query.all()
        
        main_meter_count = 0
        ac_meter_count = 0
        
        # 按房号分组（因为总表是按房号级别）
        room_no_dict: Dict[str, List[Room]] = {}
        for room in rooms:
            key = f"{room.building_id}_{room.room_no}"
            if key not in room_no_dict:
                room_no_dict[key] = []
            room_no_dict[key].append(room)
        
        # 为每个房号创建总表记录
        for key, room_list in room_no_dict.items():
            first_room = room_list[0]
            
            # 检查是否已存在
            existing_main = (
                self.db.query(RoomMainMeterRecord)
                .filter(
                    and_(
                        RoomMainMeterRecord.building_id == first_room.building_id,
                        RoomMainMeterRecord.room_no == first_room.room_no,
                        RoomMainMeterRecord.month == month,
                    )
                )
                .first()
            )
            
            if not existing_main:
                # 获取上月读数
                prev_reading = self._get_previous_main_reading(
                    first_room.building_id, first_room.room_no, month
                )
                
                main_record = RoomMainMeterRecord(
                    building_id=first_room.building_id,
                    room_no=first_room.room_no,
                    month=month,
                    meter_no=None,
                    previous_reading=prev_reading,
                    current_reading=prev_reading,
                    electricity_price=Decimal("0.49"),
                    status="pending",
                )
                self.db.add(main_record)
                main_meter_count += 1
        
        # 为每个房间创建空调表记录
        for room in rooms:
            existing_ac = (
                self.db.query(MeterRecord)
                .filter(
                    and_(
                        MeterRecord.room_id == room.id,
                        MeterRecord.month == month,
                    )
                )
                .first()
            )
            
            if not existing_ac:
                # 获取上月空调读数
                prev_ac_reading = self._get_previous_ac_reading(room.id, month)
                
                ac_record = MeterRecord(
                    room_id=room.id,
                    building_id=room.building_id,
                    month=month,
                    ac_meter_no=None,
                    ac_previous_reading=prev_ac_reading,
                    ac_current_reading=prev_ac_reading,
                    electricity_price=Decimal("0.49"),
                    # 普通表字段初始化为0
                    previous_reading=Decimal("0"),
                    current_reading=Decimal("0"),
                )
                self.db.add(ac_record)
                ac_meter_count += 1
        
        self.db.commit()
        
        return {
            "main_meter_count": main_meter_count,
            "ac_meter_count": ac_meter_count,
        }
    
    def get_combined_meter_list(
        self,
        building_id: Optional[int] = None,
        month: Optional[date] = None,
        room_no: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Dict[str, Any]:
        """获取合并后的电表列表（总表+空调表）"""
        # 基础查询条件
        main_conditions = []
        
        if building_id:
            main_conditions.append(RoomMainMeterRecord.building_id == building_id)
        
        if month:
            main_conditions.append(RoomMainMeterRecord.month == month)
        
        if room_no:
            main_conditions.append(RoomMainMeterRecord.room_no.like(f"%{room_no}%"))
        
        # 查询总表记录
        main_query = self.db.query(RoomMainMeterRecord)
        if main_conditions:
            main_query = main_query.filter(and_(*main_conditions))
        
        # 获取总记录数
        total = main_query.count()
        
        # 分页查询
        main_records = (
            main_query.order_by(
                RoomMainMeterRecord.building_id,
                RoomMainMeterRecord.room_no,
                RoomMainMeterRecord.month.desc()
            )
            .offset(skip)
            .limit(limit)
            .all()
        )
        
        # 为每个房号查询对应的空调表记录
        combined_items = []
        for main_record in main_records:
            # 查询该房号下所有房间的空调表记录
            ac_records = (
                self.db.query(MeterRecord)
                .join(Room, Room.id == MeterRecord.room_id)
                .filter(
                    and_(
                        MeterRecord.building_id == main_record.building_id,
                        MeterRecord.month == main_record.month,
                        Room.room_no == main_record.room_no,
                    )
                )
                .all()
            )
            
            # 构建空调表数据（包含入住人数）
            room_ac_records = []
            for rec in ac_records:
                # 查询该套间在当月的入住人数
                occupants_count = (
                    self.db.query(ResidenceRecord)
                    .filter(
                        and_(
                            ResidenceRecord.room_id == rec.room_id,
                            ResidenceRecord.check_in_date <= main_record.month,
                            or_(
                                ResidenceRecord.check_out_date.is_(None),
                                ResidenceRecord.check_out_date >= main_record.month,
                            ),
                            ResidenceRecord.status == "valid",
                        )
                    )
                    .count()
                )
                
                room_ac_records.append({
                    "room_id": rec.room_id,
                    "room_unit": rec.room.room_unit if rec.room else None,
                    "ac_meter_no": rec.ac_meter_no,
                    "ac_previous_reading": float(rec.ac_previous_reading or 0),
                    "ac_current_reading": float(rec.ac_current_reading or 0),
                    "ac_degree": float(rec.ac_degree or 0),
                    "ac_fee": float(rec.ac_fee or 0),
                    "occupants": occupants_count,
                })
            
            combined_items.append({
                "building_id": main_record.building_id,
                "room_no": main_record.room_no,
                "month": main_record.month,
                # 总表数据
                "main_meter_no": main_record.meter_no,
                "main_previous_reading": float(main_record.previous_reading or 0),
                "main_current_reading": float(main_record.current_reading or 0),
                "main_total_degree": float(main_record.total_degree or 0),
                "main_total_fee": float(main_record.total_fee or 0),
                # 空调表数据（数组）
                "ac_meters": room_ac_records,
                # 汇总
                "status": main_record.status,
                "remark": main_record.remark,
            })
        
        return {
            "items": combined_items,
            "total": total,
            "skip": skip,
            "limit": limit,
        }
    
    def update_main_meter(
        self,
        building_id: int,
        room_no: str,
        month: date,
        current_reading: Optional[Decimal] = None,
        meter_no: Optional[str] = None,
        remark: Optional[str] = None,
    ) -> RoomMainMeterRecord:
        """更新房号总表读数"""
        # 查找或创建记录
        record = (
            self.db.query(RoomMainMeterRecord)
            .filter(
                and_(
                    RoomMainMeterRecord.building_id == building_id,
                    RoomMainMeterRecord.room_no == room_no,
                    RoomMainMeterRecord.month == month,
                )
            )
            .first()
        )
        
        if not record:
            # 创建新记录，自动获取上月读数
            prev_reading = self._get_previous_main_reading(
                building_id, room_no, month
            )
            record = RoomMainMeterRecord(
                building_id=building_id,
                room_no=room_no,
                month=month,
                meter_no=meter_no,
                previous_reading=prev_reading,
                current_reading=current_reading or prev_reading,
                electricity_price=Decimal("0.49"),
                status="pending",
            )
            self.db.add(record)
        else:
            # 更新现有记录
            if current_reading is not None:
                record.current_reading = current_reading
            if meter_no is not None:
                record.meter_no = meter_no
            if remark is not None:
                record.remark = remark
        
        # 计算用电量和费用
        record.total_degree = record.current_reading - record.previous_reading
        record.total_fee = record.total_degree * record.electricity_price
        
        if record.current_reading > record.previous_reading:
            record.status = "recorded"
        
        self.db.commit()
        self.db.refresh(record)
        return record
    
    def update_ac_meter(
        self,
        room_id: int,
        month: date,
        ac_current_reading: Optional[Decimal] = None,
        ac_meter_no: Optional[str] = None,
    ) -> MeterRecord:
        """更新房间空调表读数"""
        # 查找或创建记录
        record = (
            self.db.query(MeterRecord)
            .filter(
                and_(
                    MeterRecord.room_id == room_id,
                    MeterRecord.month == month,
                )
            )
            .first()
        )
        
        if not record:
            # 获取房间信息
            room = self.db.query(Room).filter(Room.id == room_id).first()
            
            if not room:
                raise ValueError(f"Room {room_id} not found")
            
            # 获取上月空调读数
            prev_ac_reading = self._get_previous_ac_reading(room_id, month)
            
            record = MeterRecord(
                room_id=room_id,
                building_id=room.building_id,
                month=month,
                ac_meter_no=ac_meter_no,
                ac_previous_reading=prev_ac_reading,
                ac_current_reading=ac_current_reading or prev_ac_reading,
                electricity_price=Decimal("0.49"),
                # 普通表字段初始化为0
                previous_reading=Decimal("0"),
                current_reading=Decimal("0"),
            )
            self.db.add(record)
        else:
            # 更新现有记录
            if ac_current_reading is not None:
                record.ac_current_reading = ac_current_reading
            if ac_meter_no is not None:
                record.ac_meter_no = ac_meter_no
        
        # 计算空调用电量和费用
        record.ac_degree = record.ac_current_reading - record.ac_previous_reading
        record.ac_fee = record.ac_degree * record.electricity_price
        
        self.db.commit()
        self.db.refresh(record)
        return record
    
    def calculate_meters(
        self,
        building_id: Optional[int] = None,
        month: Optional[date] = None,
    ) -> Dict[str, int]:
        """批量计算电表费用"""
        conditions = [RoomMainMeterRecord.status == "recorded"]
        
        if building_id:
            conditions.append(RoomMainMeterRecord.building_id == building_id)
        if month:
            conditions.append(RoomMainMeterRecord.month == month)
        
        # 更新总表状态
        main_records = (
            self.db.query(RoomMainMeterRecord)
            .filter(and_(*conditions))
            .all()
        )
        
        main_count = 0
        for record in main_records:
            record.status = "calculated"
            main_count += 1
        
        self.db.commit()
        
        return {
            "main_meters_calculated": main_count,
            "ac_meters_calculated": 0,  # 空调表无需单独计算状态
        }
    
    def _get_previous_main_reading(
        self, building_id: int, room_no: str, current_month: date
    ) -> Decimal:
        """获取上月总表读数"""
        from ..utils.date_utils import add_months
        
        prev_month = add_months(current_month, -1)
        record = (
            self.db.query(RoomMainMeterRecord)
            .filter(
                and_(
                    RoomMainMeterRecord.building_id == building_id,
                    RoomMainMeterRecord.room_no == room_no,
                    RoomMainMeterRecord.month == prev_month,
                )
            )
            .first()
        )
        
        return record.current_reading if record else Decimal("0")
    
    def _get_previous_ac_reading(
        self, room_id: int, current_month: date
    ) -> Decimal:
        """获取上月空调表读数"""
        from ..utils.date_utils import add_months
        
        prev_month = add_months(current_month, -1)
        record = (
            self.db.query(MeterRecord)
            .filter(
                and_(
                    MeterRecord.room_id == room_id,
                    MeterRecord.month == prev_month,
                )
            )
            .first()
        )
        
        return record.ac_current_reading if record else Decimal("0")
