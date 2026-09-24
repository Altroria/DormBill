"""首页 Dashboard API"""
from datetime import date, timedelta
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from ..database import get_db
from ..models import (
    Building, Room, Employee, ResidenceRecord,
    MeterRecord, WaterMeterRecord, MonthlySettlement,
)
from ..utils.date_utils import parse_date, month_start, add_months
from ..services.settlement_service import calculate_realtime_settlements


router = APIRouter()


@router.get("/dashboard")
def dashboard(
    month: str = Query(None, description="YYYY-MM，缺省取当前月"),
    db: Session = Depends(get_db),
):
    """首页仪表盘数据"""
    if month:
        target_month = month_start(parse_date(month + "-01"))
    else:
        today = date.today()
        target_month = today.replace(day=1)

    # 基础统计
    building_count = db.query(Building).filter(
        Building.deleted_at.is_(None), Building.status == "active"
    ).count()
    room_count = db.query(Room).filter(
        Room.deleted_at.is_(None)
    ).count()
    employee_count = db.query(Employee).filter(
        Employee.deleted_at.is_(None), Employee.status == "active"
    ).count()

    # 当前在住人数
    current_residents = db.query(ResidenceRecord).filter(
        and_(
            ResidenceRecord.status != "invalid",
            ResidenceRecord.check_in_date <= target_month,
            or_(
                ResidenceRecord.check_out_date.is_(None),
                ResidenceRecord.check_out_date >= target_month,
            ),
        )
    ).count()

    # 试用期内人数（7天内到期）
    probation_expiring = []
    residences = db.query(ResidenceRecord).filter(
        and_(
            ResidenceRecord.status == "valid",
            ResidenceRecord.probation_months > 0,
            ResidenceRecord.check_out_date.is_(None),
        )
    ).all()
    for r in residences:
        probation_end = add_months(r.check_in_date, r.probation_months)
        days_left = (probation_end - target_month).days
        if 0 <= days_left <= 7:
            probation_expiring.append({
                "residence_id": r.id,
                "employee_id": r.employee_id,
                "probation_end": probation_end.isoformat(),
                "days_left": days_left,
            })

    # 本月数据
    month_meter_count = db.query(MeterRecord).filter(
        MeterRecord.month == target_month
    ).count()
    total_rooms = room_count
    meter_progress = f"{month_meter_count}/{total_rooms}"

    # 本月结算统计（实时计算，不依赖已保存的结算记录）
    try:
        realtime_settlements = calculate_realtime_settlements(
            db, target_month, water_mode="double"
        )
        total_rent = sum(s["rent_actual"] for s in realtime_settlements)
        total_electricity = sum(s["electricity_fee"] for s in realtime_settlements)
        total_ac = sum(s["ac_electricity_fee"] for s in realtime_settlements)
        total_water = sum(s["water_fee"] for s in realtime_settlements)
        total_deduction = sum(s["total_amount"] for s in realtime_settlements)
    except Exception as e:
        # 计算失败时返回0，避免阻断整个接口
        import traceback
        print(f"实时计算结算失败: {e}")
        print(traceback.format_exc())
        total_rent = 0
        total_electricity = 0
        total_ac = 0
        total_water = 0
        total_deduction = 0

    # 空闲房间列表（没有当前有效入住记录的房间）
    today = date.today()
    all_rooms = db.query(Room, Building).join(
        Building, Room.building_id == Building.id
    ).filter(Room.deleted_at.is_(None)).all()
    
    idle_room_list = []
    for room, building in all_rooms:
        # 查询是否有当前有效的入住记录
        has_resident = db.query(ResidenceRecord).filter(
            and_(
                ResidenceRecord.room_id == room.id,
                ResidenceRecord.status != "invalid",
                ResidenceRecord.check_in_date <= today,
                or_(
                    ResidenceRecord.check_out_date.is_(None),
                    ResidenceRecord.check_out_date >= today,
                ),
            )
        ).first()
        
        if not has_resident:
            idle_room_list.append({
                "id": room.id,
                "building_id": room.building_id,
                "building_no": building.building_no,
                "building_name": building.name,
                "room_no": room.room_no,
                "room_name": room.room_name,
                "rent_standard": float(room.rent_standard) if room.rent_standard else 0,
            })
        
        if len(idle_room_list) >= 20:
            break

    return {
        "current_month": target_month.isoformat()[:7],
        "summary": {
            "building_count": building_count,
            "room_count": room_count,
            "employee_count": employee_count,
            "current_residents": current_residents,
            "meter_progress": meter_progress,
        },
        "amounts": {
            "rent_total": round(total_rent, 2),
            "electricity_total": round(total_electricity, 2),
            "ac_electricity_total": round(total_ac, 2),
            "water_total": round(total_water, 2),
            "settlement_total": round(total_deduction, 2),
        },
        "probation_expiring": probation_expiring,
        "idle_rooms": idle_room_list,
    }


