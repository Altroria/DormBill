"""首页 Dashboard API"""
from datetime import date, timedelta
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from ..database import get_db
from ..models import (
    Building, Room, Employee, ResidenceRecord,
    MeterRecord, WaterExpense, WaterAllocation, MonthlySettlement,
)
from ..utils.date_utils import parse_date, month_start, add_months


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
        Room.deleted_at.is_(None), Room.status == "active"
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

    # 本月结算统计
    settlements = db.query(MonthlySettlement).filter(
        MonthlySettlement.month == target_month
    ).all()
    total_rent = sum(float(s.rent_actual or 0) for s in settlements)
    total_electricity = sum(float(s.electricity_fee or 0) for s in settlements)
    total_ac = sum(float(s.ac_electricity_fee or 0) for s in settlements)
    total_water = sum(float(s.water_fee or 0) for s in settlements)
    total_deduction = sum(float(s.total_amount or 0) for s in settlements)

    # 水费周期
    recent_water = db.query(WaterExpense).order_by(
        WaterExpense.period_start.desc()
    ).limit(5).all()
    water_summary = [
        {
            "id": we.id,
            "building_id": we.building_id,
            "period_start": we.period_start.isoformat(),
            "period_end": we.period_end.isoformat(),
            "total_amount": float(we.total_amount) if we.total_amount else 0,
            "status": we.status,
        }
        for we in recent_water
    ]

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
        "recent_water": water_summary,
    }


