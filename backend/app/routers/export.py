"""Excel 导出 API"""
from io import BytesIO
from datetime import date
from urllib.parse import quote
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import (
    MonthlySettlement, MeterRecord, WaterExpense, WaterAllocation,
    Employee, Room, Building,
)
from ..services.excel_service import (
    export_settlement_excel, export_meter_detail_excel,
    export_water_detail_excel,
)
from ..utils.date_utils import parse_date, month_start


router = APIRouter()


@router.get("/settlement")
def export_settlement(
    month: str = Query(..., description="YYYY-MM"),
    water_mode: str = Query("double", description="水费模式: single=单月, double=双月"),
    db: Session = Depends(get_db),
):
    """导出员工扣款表（实时计算）"""
    target_month = month_start(parse_date(month + "-01"))
    
    # 验证 water_mode
    if water_mode not in ["single", "double"]:
        water_mode = "double"
    
    # 导入实时计算函数
    from ..services.settlement_service import calculate_realtime_settlements
    
    # 实时计算结算数据
    settlements = calculate_realtime_settlements(db, target_month, water_mode)
    
    # 转换为导出格式
    items = []
    for s in settlements:
        emp = db.query(Employee).filter(Employee.id == s['employee_id']).first()
        room = db.query(Room).filter(Room.id == s['room_id']).first()
        items.append({
            "building_no": s.get('building_no', ''),
            "room_no": s.get('room_no', ''),
            "room_unit": room.room_unit if (room and hasattr(room, 'room_unit')) else "",
            "room_name": s.get('room_name', ''),
            "employee_no": s.get('employee_no', ''),
            "employee_name": s.get('employee_name', ''),
            "company": s.get('company', ''),
            "department": s.get('department', ''),
            "position": s.get('position', ''),
            "remark": s.get('remark', '') or (emp.remark if emp else ""),
            "rent_should": s.get('rent_should', 0),
            "rent_actual": s.get('rent_actual', 0),
            "electricity_fee": s.get('electricity_fee', 0),
            "ac_electricity_fee": s.get('ac_electricity_fee', 0),
            "water_fee": s.get('water_fee', 0),
            "deduction_minus": s.get('deduction_minus', 0),
            "deduction_plus": s.get('deduction_plus', 0),
            "total_amount": s.get('total_amount', 0),
        })

    bio = export_settlement_excel(items)
    water_suffix = "双月" if water_mode == "double" else "单月"
    filename = f"扣款表_{month}_{water_suffix}.xlsx"
    encoded_filename = quote(filename)
    return StreamingResponse(
        BytesIO(bio),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename*=UTF-8\'\'{encoded_filename}'},
    )


@router.get("/meter-detail")
def export_meter_detail(
    month: str = Query(..., description="YYYY-MM"),
    db: Session = Depends(get_db),
):
    """导出房间电费明细"""
    target_month = month_start(parse_date(month + "-01"))
    rows = db.query(MeterRecord).filter(
        MeterRecord.month == target_month
    ).all()

    items = []
    for m in rows:
        room = db.query(Room).filter(Room.id == m.room_id).first()
        building = None
        if room:
            building = db.query(Building).filter(Building.id == room.building_id).first()
        items.append({
            "building_no": building.building_no if building else "",
            "room_no": room.room_no if room else "",
            "room_name": room.room_name if room else "",
            "meter_no": room.meter_no if room else "",
            "previous_reading": float(m.previous_reading) if m.previous_reading else 0,
            "current_reading": float(m.current_reading) if m.current_reading else 0,
            "total_degree": float(m.total_degree) if m.total_degree else 0,
            "electricity_price": float(m.electricity_price) if m.electricity_price else 0,
            "total_fee": float(m.total_fee) if m.total_fee else 0,
            "ac_previous_reading": float(m.ac_previous_reading) if m.ac_previous_reading else 0,
            "ac_current_reading": float(m.ac_current_reading) if m.ac_current_reading else 0,
            "ac_degree": float(m.ac_degree) if m.ac_degree else 0,
            "ac_unit_price": float(m.ac_unit_price) if m.ac_unit_price else 0,
            "ac_fee": float(m.ac_fee) if m.ac_fee else 0,
        })

    bio = export_meter_detail_excel(items)
    filename = f"电费明细_{month}.xlsx"
    encoded_filename = quote(filename)
    return StreamingResponse(
        BytesIO(bio),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename*=UTF-8\'\'{encoded_filename}'},
    )


@router.get("/water-detail")
def export_water_detail(
    period: str = Query(..., description="YYYY-MM 起始月"),
    db: Session = Depends(get_db),
):
    """导出水费分摊明细"""
    target_period = month_start(parse_date(period + "-01"))
    rows = db.query(WaterExpense).filter(
        WaterExpense.period_start <= target_period,
        WaterExpense.period_end >= target_period,
    ).all()

    items = []
    for we in rows:
        allocs = db.query(WaterAllocation).filter(
            WaterAllocation.water_expense_id == we.id
        ).all()
        for a in allocs:
            emp = db.query(Employee).filter(Employee.id == a.employee_id).first()
            room = db.query(Room).filter(Room.id == a.room_id).first()
            building = None
            if room:
                building = db.query(Building).filter(Building.id == room.building_id).first()
            items.append({
                "period_start": we.period_start.isoformat(),
                "period_end": we.period_end.isoformat(),
                "building_no": building.building_no if building else "",
                "room_no": room.room_no if room else "",
                "room_name": room.room_name if room else "",
                "employee_name": emp.name if emp else "",
                "month1_days": a.month1_days,
                "month2_days": a.month2_days,
                "is_valid": a.is_valid,
                "amount": float(a.amount) if a.amount else 0,
                "remark": a.remark or "",
            })

    bio = export_water_detail_excel(items)
    filename = f"水费明细_{period}.xlsx"
    encoded_filename = quote(filename)
    return StreamingResponse(
        BytesIO(bio),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename*=UTF-8\'\'{encoded_filename}'},
    )
