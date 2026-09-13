"""电表管理V2路由（总表+空调表分离）"""
from datetime import date
from decimal import Decimal
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..services.meter_v2_service import MeterV2Service
from ..services.electricity_calculation_service import ElectricityCalculationService
from ..schemas.meter_v2 import (
    CombinedMeterListResponse,
    MainMeterUpdateRequest,
    AcMeterUpdateRequest,
    MeterCalculateRequest,
    MeterCalculateResponse,
    InitMonthRequest,
    InitMonthResponse,
    BatchUpdateRequest,
    BatchUpdateResponse,
    EnhancedCalculateRequest,
    EnhancedCalculateResponse,
    EnhancedMeterListResponse,
)

router = APIRouter(prefix="/meters-v2", tags=["电表管理V2"])


@router.post("/init-month", response_model=InitMonthResponse)
def init_month(
    data: InitMonthRequest,
    db: Session = Depends(get_db),
):
    """初始化月度电表记录"""
    service = MeterV2Service(db)
    
    # 转换月份字符串为date对象
    month_date = date.fromisoformat(f"{data.month}-01")
    
    result = service.init_month(
        month=month_date,
        building_id=data.building_id,
    )
    
    return result


@router.get("/combined", response_model=CombinedMeterListResponse)
def get_combined_meters(
    month: str = Query(..., description="月份 YYYY-MM"),
    building_id: Optional[int] = Query(None, description="楼栋ID"),
    room_no: Optional[str] = Query(None, description="房号（模糊查询）"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """获取组合电表列表（总表+空调表）"""
    try:
        service = MeterV2Service(db)
        
        # 转换月份字符串为date对象
        month_date = date.fromisoformat(f"{month}-01")
        
        result = service.get_combined_meter_list(
            building_id=building_id,
            month=month_date,
            room_no=room_no,
            skip=skip,
            limit=limit,
        )
        
        return result
    except Exception as e:
        import traceback
        print(f"Error in get_combined_meters: {e}")
        print(traceback.format_exc())
        raise


@router.put("/main/{building_id}/{room_no}/{month}")
def update_main_meter(
    building_id: int,
    room_no: str,
    month: str,
    data: MainMeterUpdateRequest,
    db: Session = Depends(get_db),
):
    """更新房号总表读数"""
    service = MeterV2Service(db)
    
    # 转换月份字符串为date对象
    month_date = date.fromisoformat(f"{month}-01")
    
    record = service.update_main_meter(
        building_id=building_id,
        room_no=room_no,
        month=month_date,
        current_reading=data.current_reading,
        meter_no=data.meter_no,
        remark=data.remark,
    )
    
    return {
        "id": record.id,
        "building_id": record.building_id,
        "room_no": record.room_no,
        "month": record.month,
        "meter_no": record.meter_no,
        "previous_reading": float(record.previous_reading),
        "current_reading": float(record.current_reading),
        "total_degree": float(record.total_degree),
        "total_fee": float(record.total_fee),
        "status": record.status,
        "remark": record.remark,
    }


@router.put("/ac/{room_id}/{month}")
def update_ac_meter(
    room_id: int,
    month: str,
    data: AcMeterUpdateRequest,
    db: Session = Depends(get_db),
):
    """更新房间空调表读数"""
    service = MeterV2Service(db)
    
    # 转换月份字符串为date对象
    month_date = date.fromisoformat(f"{month}-01")
    
    record = service.update_ac_meter(
        room_id=room_id,
        month=month_date,
        ac_current_reading=data.ac_current_reading,
        ac_meter_no=data.ac_meter_no,
    )
    
    return {
        "id": record.id,
        "room_id": record.room_id,
        "month": record.month,
        "ac_meter_no": record.ac_meter_no,
        "ac_previous_reading": float(record.ac_previous_reading),
        "ac_current_reading": float(record.ac_current_reading),
        "ac_degree": float(record.ac_degree),
        "ac_fee": float(record.ac_fee),
    }


@router.post("/calculate", response_model=MeterCalculateResponse)
def calculate_meters(
    data: MeterCalculateRequest,
    db: Session = Depends(get_db),
):
    """批量计算电表费用"""
    service = MeterV2Service(db)
    
    # 转换月份字符串为date对象
    month_date = None
    if data.month:
        month_date = date.fromisoformat(f"{data.month}-01")
    
    result = service.calculate_meters(
        building_id=data.building_id,
        month=month_date,
    )
    
    return result


@router.put("/ac-batch/{month}")
def batch_update_ac_meters(
    month: str,
    data: list[AcMeterUpdateRequest],
    db: Session = Depends(get_db),
):
    """批量更新空调表读数"""
    service = MeterV2Service(db)
    
    # 转换月份字符串为date对象
    month_date = date.fromisoformat(f"{month}-01")
    
    updated_count = 0
    for item in data:
        service.update_ac_meter(
            room_id=item.room_id,
            month=month_date,
            ac_current_reading=item.ac_current_reading,
            ac_meter_no=item.ac_meter_no,
        )
        updated_count += 1
    
    return {
        "message": f"成功更新 {updated_count} 条空调表记录",
        "count": updated_count
    }


@router.put("/batch-update", response_model=BatchUpdateResponse)
def batch_update_meters(
    data: BatchUpdateRequest,
    db: Session = Depends(get_db),
):
    """
    批量更新电表（总表+空调表）
    
    一次性提交整个房号的所有电表数据，减少网络请求
    """
    service = MeterV2Service(db)
    
    # 转换月份字符串为date对象
    month_date = date.fromisoformat(f"{data.month}-01")
    
    main_meters_updated = 0
    ac_meters_updated = 0
    
    for room_update in data.updates:
        # 更新总表
        service.update_main_meter(
            building_id=room_update.building_id,
            room_no=room_update.room_no,
            month=month_date,
            current_reading=room_update.main_current_reading,
            meter_no=room_update.main_meter_no,
        )
        main_meters_updated += 1
        
        # 更新所有空调表
        for ac_update in room_update.ac_meters:
            service.update_ac_meter(
                room_id=ac_update.room_id,
                month=month_date,
                ac_current_reading=ac_update.ac_current_reading,
            )
            ac_meters_updated += 1
    
    return BatchUpdateResponse(
        main_meters_updated=main_meters_updated,
        ac_meters_updated=ac_meters_updated,
        message=f"成功更新 {main_meters_updated} 个房号总表和 {ac_meters_updated} 个空调表"
    )


@router.post("/calculate-enhanced", response_model=EnhancedCalculateResponse)
def calculate_meters_enhanced(
    data: EnhancedCalculateRequest,
    db: Session = Depends(get_db),
):
    """
    增强的电表计算接口
    
    自动计算：
    1. 公共用电（总表 - 空调表）
    2. 个人分摊（按人数分配公共电费和空调费）
    """
    calc_service = ElectricityCalculationService(db)
    
    # 转换月份字符串为date对象
    month_date = date.fromisoformat(f"{data.month}-01")
    
    result = calc_service.calculate_all_meters(
        month=month_date,
        building_id=data.building_id,
    )
    
    return EnhancedCalculateResponse(**result)


@router.get("/list-enhanced", response_model=EnhancedMeterListResponse)
def get_enhanced_meter_list(
    month: str = Query(..., description="月份 YYYY-MM"),
    building_id: Optional[int] = Query(None, description="楼栋ID"),
    room_no: Optional[str] = Query(None, description="房号（模糊查询）"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """
    获取增强的电表列表（包含公共用电、人均费用等统计信息）- 优化版
    """
    from sqlalchemy import and_, func as sql_func
    from ..models.room_main_meter import RoomMainMeterRecord
    from ..models.meter import MeterRecord
    from ..models.room import Room
    from ..models.building import Building
    from ..models.residence import ResidenceRecord
    from ..utils.date_utils import month_start, stay_days_in_month
    
    # 转换月份字符串为date对象
    month_date = date.fromisoformat(f"{month}-01")
    
    # 查询总表记录
    query = db.query(RoomMainMeterRecord).filter(
        RoomMainMeterRecord.month == month_date
    )
    
    if building_id:
        query = query.filter(RoomMainMeterRecord.building_id == building_id)
    
    if room_no:
        query = query.filter(RoomMainMeterRecord.room_no.like(f"%{room_no}%"))
    
    # 总数
    total = query.count()
    
    # 分页
    main_meters = query.offset(skip).limit(limit).all()
    
    # 批量预加载数据，避免N+1查询
    building_ids = list(set(m.building_id for m in main_meters))
    room_filters = [(m.building_id, m.room_no) for m in main_meters]
    
    # 批量查询楼栋
    buildings_dict = {
        b.id: b for b in db.query(Building).filter(Building.id.in_(building_ids)).all()
    } if building_ids else {}
    
    # 批量查询空调表
    ac_meters_list = []
    if room_filters:
        for bldg_id, rm_no in room_filters:
            ac_meters = (
                db.query(MeterRecord)
                .join(Room, Room.id == MeterRecord.room_id)
                .filter(
                    and_(
                        MeterRecord.building_id == bldg_id,
                        Room.room_no == rm_no,
                        MeterRecord.month == month_date,
                    )
                )
                .all()
            )
            ac_meters_list.append(((bldg_id, rm_no), ac_meters))
    
    ac_meters_dict = dict(ac_meters_list)
    
    # 批量查询房间
    rooms_list = []
    if room_filters:
        for bldg_id, rm_no in room_filters:
            rooms = (
                db.query(Room)
                .filter(
                    and_(
                        Room.building_id == bldg_id,
                        Room.room_no == rm_no,
                        Room.status == "active",
                    )
                )
                .all()
            )
            rooms_list.append(((bldg_id, rm_no), rooms))
    
    rooms_dict = dict(rooms_list)
    
    # 批量查询所有相关的room_ids的入住记录
    all_room_ids = []
    for rooms in rooms_dict.values():
        all_room_ids.extend([r.id for r in rooms])
    
    residence_records_dict = {}
    if all_room_ids:
        all_records = (
            db.query(ResidenceRecord)
            .filter(
                and_(
                    ResidenceRecord.room_id.in_(all_room_ids),
                    ResidenceRecord.status.in_(["valid", "business_trip"]),
                )
            )
            .all()
        )
        
        # 按room_id分组
        for record in all_records:
            if record.room_id not in residence_records_dict:
                residence_records_dict[record.room_id] = []
            residence_records_dict[record.room_id].append(record)
    
    items = []
    for main_meter in main_meters:
        key = (main_meter.building_id, main_meter.room_no)
        
        # 获取楼栋信息
        building = buildings_dict.get(main_meter.building_id)
        
        # 获取该房号下所有空调表
        ac_meters = ac_meters_dict.get(key, [])
        
        # 空调汇总
        total_ac_degree = sum(float(m.ac_degree) for m in ac_meters)
        total_ac_fee = sum(float(m.ac_fee) for m in ac_meters)
        
        # 获取房号内所有房间
        rooms = rooms_dict.get(key, [])
        room_ids = [r.id for r in rooms]
        
        # 统计入住人数
        total_occupants = 0
        if room_ids:
            for room_id in room_ids:
                records = residence_records_dict.get(room_id, [])
                for r in records:
                    days = stay_days_in_month(r.check_in_date, r.check_out_date, month_date)
                    if days > 0:
                        total_occupants += 1
        
        # 计算人均公共电费
        common_fee_per_person = (
            float(main_meter.common_fee) / total_occupants if total_occupants > 0 else 0
        )
        
        # 构建空调表信息
        ac_meters_info = []
        for ac_meter in ac_meters:
            # 从rooms中查找对应的room
            room = next((r for r in rooms if r.id == ac_meter.room_id), None)
            
            # 统计该套间人数
            occupants_count = 0
            occupants = residence_records_dict.get(ac_meter.room_id, [])
            for occ in occupants:
                days = stay_days_in_month(occ.check_in_date, occ.check_out_date, month_date)
                if days > 0:
                    occupants_count += 1
            
            ac_meters_info.append({
                "room_id": ac_meter.room_id,
                "room_unit": room.room_unit if room else None,
                "ac_meter_no": ac_meter.ac_meter_no,
                "ac_previous_reading": float(ac_meter.ac_previous_reading),
                "ac_current_reading": float(ac_meter.ac_current_reading),
                "ac_degree": float(ac_meter.ac_degree),
                "ac_fee": float(ac_meter.ac_fee),
                "occupants": occupants_count,
            })
        
        items.append({
            "building_id": main_meter.building_id,
            "building_no": building.building_no if building else None,
            "room_no": main_meter.room_no,
            "month": main_meter.month,
            "main_total_degree": float(main_meter.total_degree),
            "main_total_fee": float(main_meter.total_fee),
            "common_degree": float(main_meter.common_degree),
            "common_fee": float(main_meter.common_fee),
            "total_ac_degree": total_ac_degree,
            "total_ac_fee": total_ac_fee,
            "ac_meters": ac_meters_info,
            "total_occupants": total_occupants,
            "common_fee_per_person": round(common_fee_per_person, 2),
            "status": main_meter.status,
        })
    
    return EnhancedMeterListResponse(items=items, total=total)
