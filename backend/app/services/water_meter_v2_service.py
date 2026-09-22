"""水费管理服务 V2 - 简化版（直接编辑水费）"""
from datetime import date
from decimal import Decimal
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func

from ..models.water import WaterMeterRecord
from ..models.room import Room
from ..models.building import Building
from ..models.residence import ResidenceRecord
from ..utils.date_utils import month_start


class WaterMeterV2Service:
    """水费管理服务 V2（简化版）"""

    def __init__(self, db: Session):
        self.db = db

    def init_month(
        self,
        month: date,
        building_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        初始化月度水费记录（按房号）
        
        Args:
            month: 月份（每月1号）
            building_id: 可选，指定楼栋ID，否则初始化所有楼栋
            
        Returns:
            {
                "water_meter_count": 98,
                "message": "成功初始化 98 个房号水费记录"
            }
        """
        month = month_start(month)
        
        # 查询所有活跃房间，按 building_id 和 room_no 分组
        query = (
            self.db.query(
                Room.building_id,
                Room.room_no,
            )
            .filter(
                Room.deleted_at.is_(None),
                Room.status == "active",
            )
            .group_by(Room.building_id, Room.room_no)
        )
        
        if building_id:
            query = query.filter(Room.building_id == building_id)
        
        room_groups = query.all()
        
        created_count = 0
        
        for room_group in room_groups:
            bld_id = room_group.building_id
            r_no = room_group.room_no
            
            # 检查是否已存在
            exists = self.db.query(WaterMeterRecord).filter(
                WaterMeterRecord.building_id == bld_id,
                WaterMeterRecord.room_no == r_no,
                WaterMeterRecord.month == month,
            ).first()
            
            if exists:
                continue
            
            # 创建新记录，水费默认为0
            new_record = WaterMeterRecord(
                building_id=bld_id,
                room_no=r_no,
                month=month,
                total_fee=Decimal("0"),
                remark=None,
            )
            
            self.db.add(new_record)
            created_count += 1
        
        self.db.commit()
        
        return {
            "water_meter_count": created_count,
            "message": f"成功初始化 {created_count} 个房号水费记录"
        }

    def get_water_meter_list(
        self,
        month: date,
        building_id: Optional[int] = None,
        room_no: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Dict[str, Any]:
        """
        获取水费列表（按房号，包含入住人数）
        
        Returns:
            {
                "items": [...],
                "total": 98
            }
        """
        month = month_start(month)
        
        # 查询水费记录
        query = (
            self.db.query(
                WaterMeterRecord,
                Building,
            )
            .join(Building, Building.id == WaterMeterRecord.building_id)
            .filter(WaterMeterRecord.month == month)
        )
        
        if building_id:
            query = query.filter(WaterMeterRecord.building_id == building_id)
        
        if room_no:
            query = query.filter(WaterMeterRecord.room_no.like(f"%{room_no}%"))
        
        # 按房号排序
        query = query.order_by(Building.building_no, WaterMeterRecord.room_no)
        
        total = query.count()
        
        records = query.offset(skip).limit(limit).all()
        
        items = []
        for water_record, building in records:
            # 统计该房号下所有单间的当月入住人数
            occupants_count = self._count_occupants_by_room_no(
                water_record.building_id,
                water_record.room_no,
                month
            )
            
            # 获取房间名称
            room = self.db.query(Room).filter(
                Room.building_id == water_record.building_id,
                Room.room_no == water_record.room_no,
                Room.deleted_at.is_(None),
            ).first()
            
            room_name = room.room_name if room else None
            
            items.append({
                "id": water_record.id,
                "room_no": water_record.room_no,
                "building_id": building.id,
                "building_no": building.building_no,
                "room_name": room_name,
                "month": water_record.month,
                "total_fee": float(water_record.total_fee),
                "remark": water_record.remark,
                "occupants_count": occupants_count,
            })
        
        return {
            "items": items,
            "total": total,
        }

    def update_water_meter(
        self,
        building_id: int,
        room_no: str,
        month: date,
        total_fee: Optional[Decimal] = None,
        remark: Optional[str] = None,
    ) -> WaterMeterRecord:
        """
        更新水费（按房号）
        
        Args:
            building_id: 楼栋ID
            room_no: 房号
            month: 月份
            total_fee: 水费金额
            remark: 备注
        """
        month = month_start(month)
        
        record = self.db.query(WaterMeterRecord).filter(
            WaterMeterRecord.building_id == building_id,
            WaterMeterRecord.room_no == room_no,
            WaterMeterRecord.month == month,
        ).first()
        
        if not record:
            raise ValueError(f"未找到房号 {room_no} 在 {month} 的水费记录")
        
        # 更新水费
        if total_fee is not None:
            record.total_fee = total_fee
        
        # 更新备注
        if remark is not None:
            record.remark = remark
        
        self.db.commit()
        self.db.refresh(record)
        
        return record

    def batch_update_water_meters(
        self,
        month: date,
        updates: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        批量更新水费（按房号）
        
        Args:
            month: 月份
            updates: 更新列表，每项包含:
                {
                    "building_id": 1,
                    "room_no": "201",
                    "total_fee": 50.00,
                    "remark": "备注",
                }
        """
        month = month_start(month)
        
        updated_count = 0
        
        for update in updates:
            self.update_water_meter(
                building_id=update["building_id"],
                room_no=update["room_no"],
                month=month,
                total_fee=update.get("total_fee"),
                remark=update.get("remark"),
            )
            updated_count += 1
        
        return {
            "updated_count": updated_count,
            "message": f"成功更新 {updated_count} 个水费记录"
        }

    def _count_occupants_by_room_no(
        self, building_id: int, room_no: str, month: date
    ) -> int:
        """统计房号下所有单间的当月入住人数"""
        # 查询该房号下的所有房间ID
        room_ids = [
            r.id for r in self.db.query(Room.id).filter(
                Room.building_id == building_id,
                Room.room_no == room_no,
                Room.deleted_at.is_(None),
            ).all()
        ]
        
        if not room_ids:
            return 0
        
        # 统计这些房间的入住人数
        count = self.db.query(ResidenceRecord).filter(
            and_(
                ResidenceRecord.room_id.in_(room_ids),
                ResidenceRecord.status.in_(["valid", "business_trip"]),
                ResidenceRecord.check_in_date <= month,
                or_(
                    ResidenceRecord.check_out_date.is_(None),
                    ResidenceRecord.check_out_date >= month,
                ),
            )
        ).count()
        
        return count
