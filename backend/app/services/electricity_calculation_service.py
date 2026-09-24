"""电费计算服务：公共用电计算 + 个人分摊逻辑"""
from decimal import Decimal
from datetime import date
from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from ..models.meter import MeterRecord
from ..models.room_main_meter import RoomMainMeterRecord
from ..models.room import Room
from ..models.residence import ResidenceRecord
from ..utils.decimal_utils import to_decimal, round_money, allocate_with_remainder
from ..utils.date_utils import month_start, stay_days_in_month


class ElectricityCalculationService:
    """电费计算服务 - 实现公共用电逻辑"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def calculate_room_no_electricity(
        self,
        building_id: int,
        room_no: str,
        month: date,
    ) -> Dict:
        """
        计算单个房号的完整电费逻辑
        
        核心逻辑：
        1. 总表用电量 - 所有空调用电量 = 公共用电
        2. 公共电费按房号内所有人数平均分摊
        3. 空调费按各套间人数分摊
        
        返回：{
            'main_meter': {...},
            'common_degree': Decimal,
            'common_fee': Decimal,
            'total_ac_degree': Decimal,
            'total_ac_fee': Decimal,
            'distributions': [...]  # 个人分摊结果
        }
        """
        month = month_start(month)
        
        # 1. 获取总表记录
        main_meter = self._get_main_meter(building_id, room_no, month)
        if not main_meter:
            raise ValueError(f"房号 {room_no} 在 {month} 月的总表记录不存在")
        
        total_degree = to_decimal(main_meter.total_degree)
        total_fee = to_decimal(main_meter.total_fee)
        
        # 2. 获取该房号下所有套间的空调表
        ac_meters = self._get_ac_meters_by_room_no(building_id, room_no, month)
        
        total_ac_degree = sum(to_decimal(m.ac_degree) for m in ac_meters)
        total_ac_fee = sum(to_decimal(m.ac_fee) for m in ac_meters)
        
        # 3. 计算公共用电（核心逻辑）
        common_degree = total_degree - total_ac_degree
        common_fee = total_fee - total_ac_fee
        
        # 4. 更新总表的公共用电字段
        main_meter.common_degree = common_degree
        main_meter.common_fee = common_fee
        main_meter.status = "calculated"
        
        # 5. 获取房号内所有有效入住人员
        occupants = self._get_all_occupants_in_room_no(building_id, room_no, month)
        
        if not occupants:
            # 没有入住人员，直接保存并返回
            self.db.commit()
            return {
                'main_meter_id': main_meter.id,
                'common_degree': float(common_degree),
                'common_fee': float(common_fee),
                'total_ac_degree': float(total_ac_degree),
                'total_ac_fee': float(total_ac_fee),
                'distributions': [],
                'total_occupants': 0,
            }
        
        # 6. 分摊公共用电费用（按人数）
        n = len(occupants)
        common_fee_allocations = allocate_with_remainder(common_fee, n)
        
        # 7. 为每个人计算套间空调费用
        distributions = []
        for idx, occupant in enumerate(occupants):
            room_id = occupant.room_id
            
            # 找到该套间的空调表
            ac_meter = next((m for m in ac_meters if m.room_id == room_id), None)
            
            if ac_meter:
                # 获取该套间的入住人数
                room_occupants = [o for o in occupants if o.room_id == room_id]
                
                # 检查是否有主缴费人
                primary_payers = [o for o in room_occupants if o.is_primary_payer == 1]
                
                if primary_payers:
                    # 夫妻间：只有主缴费人承担空调费
                    if occupant.is_primary_payer == 1:
                        personal_ac_fee = to_decimal(ac_meter.ac_fee)
                    else:
                        personal_ac_fee = Decimal("0")
                else:
                    # 普通情况：按套间人数分摊空调费
                    room_occupants_count = len(room_occupants)
                    ac_fee_allocations = allocate_with_remainder(
                        to_decimal(ac_meter.ac_fee),
                        room_occupants_count
                    )
                    room_idx = room_occupants.index(occupant)
                    personal_ac_fee = ac_fee_allocations[room_idx]
            else:
                personal_ac_fee = Decimal("0")
            
            # 个人总电费
            personal_common_fee = common_fee_allocations[idx]
            personal_total_fee = personal_common_fee + personal_ac_fee
            
            distributions.append({
                'employee_id': occupant.employee_id,
                'room_id': occupant.room_id,
                'common_electricity_fee': round_money(personal_common_fee),
                'ac_electricity_fee': round_money(personal_ac_fee),
                'total_electricity_fee': round_money(personal_total_fee),
            })
        
        self.db.commit()
        
        return {
            'main_meter_id': main_meter.id,
            'building_id': building_id,
            'room_no': room_no,
            'month': month,
            'common_degree': float(common_degree),
            'common_fee': float(common_fee),
            'total_ac_degree': float(total_ac_degree),
            'total_ac_fee': float(total_ac_fee),
            'distributions': distributions,
            'total_occupants': n,
            'common_fee_per_person': float(round_money(common_fee / n)) if n > 0 else 0,
        }
    
    def calculate_all_meters(
        self,
        month: date,
        building_id: Optional[int] = None,
    ) -> Dict:
        """
        批量计算所有房号的电费
        
        返回统计信息
        """
        month = month_start(month)
        
        # 查询所有总表记录
        query = self.db.query(RoomMainMeterRecord).filter(
            RoomMainMeterRecord.month == month
        )
        
        if building_id:
            query = query.filter(RoomMainMeterRecord.building_id == building_id)
        
        main_meters = query.all()
        
        calculated_count = 0
        total_common_fee = Decimal("0")
        total_ac_fee = Decimal("0")
        distributions_created = 0
        
        for main_meter in main_meters:
            try:
                result = self.calculate_room_no_electricity(
                    main_meter.building_id,
                    main_meter.room_no,
                    month
                )
                calculated_count += 1
                total_common_fee += Decimal(str(result['common_fee']))
                total_ac_fee += Decimal(str(result['total_ac_fee']))
                distributions_created += len(result['distributions'])
            except Exception as e:
                print(f"计算房号 {main_meter.room_no} 失败: {e}")
                continue
        
        return {
            'main_meters_calculated': calculated_count,
            'distributions_created': distributions_created,
            'total_common_fee': float(round_money(total_common_fee)),
            'total_ac_fee': float(round_money(total_ac_fee)),
            'total_fee': float(round_money(total_common_fee + total_ac_fee)),
        }
    
    def _get_main_meter(
        self,
        building_id: int,
        room_no: str,
        month: date,
    ) -> Optional[RoomMainMeterRecord]:
        """获取总表记录"""
        return (
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
    
    def _get_ac_meters_by_room_no(
        self,
        building_id: int,
        room_no: str,
        month: date,
    ) -> List[MeterRecord]:
        """获取该房号下所有套间的空调表"""
        return (
            self.db.query(MeterRecord)
            .join(Room, Room.id == MeterRecord.room_id)
            .filter(
                and_(
                    MeterRecord.building_id == building_id,
                    Room.room_no == room_no,
                    MeterRecord.month == month,
                )
            )
            .all()
        )
    
    def _get_all_occupants_in_room_no(
        self,
        building_id: int,
        room_no: str,
        month: date,
    ) -> List[ResidenceRecord]:
        """
        获取房号内所有有效入住人员
        
        有效入住：
        - 状态为 valid
        - 在该月有入住天数
        - 非出差状态参与电费分摊
        """
        # 查询该房号下所有房间
        rooms = (
            self.db.query(Room)
            .filter(
                and_(
                    Room.building_id == building_id,
                    Room.room_no == room_no,
                    Room.status == "active",
                )
            )
            .all()
        )
        
        room_ids = [r.id for r in rooms]
        
        if not room_ids:
            return []
        
        # 查询入住记录
        records = (
            self.db.query(ResidenceRecord)
            .filter(
                and_(
                    ResidenceRecord.room_id.in_(room_ids),
                    ResidenceRecord.status.in_(["valid", "business_trip"]),
                )
            )
            .all()
        )
        
        # 过滤：在该月有入住天数
        valid_occupants = []
        for r in records:
            days = stay_days_in_month(r.check_in_date, r.check_out_date, month)
            if days > 0:
                valid_occupants.append(r)
        
        return valid_occupants


__all__ = ["ElectricityCalculationService"]
