"""月度结算 API"""
from typing import Optional
from decimal import Decimal
from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_

from ..database import get_db
from ..models import (
    MonthlySettlement, Employee, Room, Building, ResidenceRecord,
)
from ..schemas.settlement import (
    SettlementUpdate, SettlementResponse, SettlementListResponse,
    SettlementGenerateRequest, PrecheckResponse, PrecheckItem, LockRequest,
)
from ..services.settlement_service import (
    precheck_settlement, generate_settlement, lock_month, unlock_month,
    recalculate_settlement,
)
from ..utils.exceptions import NotFoundError, BusinessError
from ..utils.date_utils import parse_date, month_start


router = APIRouter()


def _to_response(s: MonthlySettlement, db: Session) -> SettlementResponse:
    data = SettlementResponse.model_validate(s)
    emp = db.query(Employee).filter(Employee.id == s.employee_id).first()
    room = db.query(Room).filter(Room.id == s.room_id).first()
    if emp:
        data.employee_name = emp.name
        data.employee_no = emp.employee_no
        data.company = emp.company
        data.department = emp.department
        data.position = emp.position
    if room:
        building = db.query(Building).filter(Building.id == room.building_id).first()
        data.room_no = room.room_no
        data.room_name = room.room_name
        data.building_id = room.building_id
        if building:
            data.building_no = building.building_no
    # 检查房间状态
    if room:
        res = db.query(ResidenceRecord).filter(
            and_(
                ResidenceRecord.room_id == room.id,
                ResidenceRecord.employee_id == s.employee_id,
            )
        ).order_by(ResidenceRecord.id.desc()).first()
        if res:
            data.room_status = res.status
    return data


@router.get("", response_model=SettlementListResponse)
def list_settlements(
    month: str = Query(..., description="YYYY-MM"),
    building_id: Optional[int] = Query(None),
    keyword: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """月度结算列表"""
    target_month = month_start(parse_date(month + "-01"))
    query = db.query(MonthlySettlement).filter(MonthlySettlement.month == target_month)
    if status:
        query = query.filter(MonthlySettlement.status == status)
    if building_id:
        query = query.filter(MonthlySettlement.room_id.in_(
            db.query(Room.id).filter(Room.building_id == building_id)
        ))
    if keyword:
        emp_ids = [
            e.id for e in db.query(Employee).filter(
                Employee.name.like(f"%{keyword}%"),
            ).all()
        ]
        if emp_ids:
            query = query.filter(MonthlySettlement.employee_id.in_(emp_ids))
        else:
            query = query.filter(MonthlySettlement.id == -1)
    rows = query.order_by(MonthlySettlement.id.asc()).all()
    items = [_to_response(s, db) for s in rows]
    return {"items": items, "total": len(items)}


@router.post("/precheck", response_model=PrecheckResponse)
def precheck(data: SettlementGenerateRequest, db: Session = Depends(get_db)):
    """生成前检查"""
    target_month = month_start(parse_date(data.month))
    result = precheck_settlement(db, target_month)
    return PrecheckResponse(
        blocking=[PrecheckItem(**item) for item in result["blocking"]],
        warnings=[PrecheckItem(**item) for item in result["warnings"]],
    )


@router.post("/generate", response_model=SettlementListResponse)
def generate(data: SettlementGenerateRequest, db: Session = Depends(get_db)):
    """生成月度结算"""
    target_month = month_start(parse_date(data.month))
    settlements = generate_settlement(db, target_month, force=data.force)
    db.commit()
    for s in settlements:
        db.refresh(s)
    items = [_to_response(s, db) for s in settlements]
    return {"items": items, "total": len(items)}


@router.post("/recalculate", response_model=SettlementListResponse)
def recalculate(data: SettlementGenerateRequest, db: Session = Depends(get_db)):
    """重新计算"""
    target_month = month_start(parse_date(data.month))
    settlements = recalculate_settlement(db, target_month)
    db.commit()
    for s in settlements:
        db.refresh(s)
    items = [_to_response(s, db) for s in settlements]
    return {"items": items, "total": len(items)}


@router.put("/{settlement_id}", response_model=SettlementResponse)
def update_settlement(
    settlement_id: int, data: SettlementUpdate, db: Session = Depends(get_db),
):
    """编辑单条结算（调整实扣房租、补扣等）"""
    s = db.query(MonthlySettlement).filter(MonthlySettlement.id == settlement_id).first()
    if not s:
        raise NotFoundError(f"结算记录不存在: {settlement_id}")
    if s.status == "locked":
        raise BusinessError("已锁定的月份不允许修改")

    update_data = data.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(s, k, v)

    # 重算最终扣款
    from ..services.rent_service import calculate_final_amount
    s.total_amount = calculate_final_amount(
        rent_actual=s.rent_actual,
        electricity_fee=s.electricity_fee,
        ac_fee=s.ac_electricity_fee,
        water_fee=s.water_fee,
        deduction_minus=s.deduction_minus,
        deduction_plus=s.deduction_plus,
    )
    db.commit()
    db.refresh(s)
    return _to_response(s, db)


@router.post("/lock")
def lock(data: LockRequest, db: Session = Depends(get_db)):
    """锁定月份"""
    target_month = month_start(parse_date(data.month))
    count = lock_month(db, target_month)
    db.commit()
    return {"message": "ok", "locked": count}


@router.post("/unlock")
def unlock(data: LockRequest, db: Session = Depends(get_db)):
    """解锁月份"""
    target_month = month_start(parse_date(data.month))
    count = unlock_month(db, target_month)
    db.commit()
    return {"message": "ok", "unlocked": count}
