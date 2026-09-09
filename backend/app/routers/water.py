"""水费 API"""
from typing import Optional
from decimal import Decimal
from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_

from ..database import get_db
from ..models import WaterExpense, WaterAllocation, Building, Room, Employee
from ..schemas.water import (
    WaterExpenseCreate, WaterExpenseUpdate, WaterExpenseResponse,
    WaterExpenseListResponse, WaterAllocationResponse, AllocationBatchUpdate,
)
from ..services.water_service import (
    allocate_water_expense, rebalance_water_allocations,
    update_water_allocation_amount,
)
from ..utils.exceptions import NotFoundError
from ..utils.date_utils import parse_date, month_start, add_months


router = APIRouter()


def _alloc_to_response(alloc: WaterAllocation, db: Session) -> WaterAllocationResponse:
    data = WaterAllocationResponse.model_validate(alloc)
    emp = db.query(Employee).filter(Employee.id == alloc.employee_id).first()
    room = db.query(Room).filter(Room.id == alloc.room_id).first()
    if emp:
        data.employee_name = emp.name
        data.employee_no = emp.employee_no
    if room:
        data.room_no = room.room_no
        data.room_name = room.room_name
        building = db.query(Building).filter(Building.id == room.building_id).first()
        if building:
            data.building_no = building.building_no
    return data


def _expense_to_response(we: WaterExpense, db: Session) -> WaterExpenseResponse:
    data = WaterExpenseResponse.model_validate(we)
    building = db.query(Building).filter(Building.id == we.building_id).first()
    if building:
        data.building_no = building.building_no
        data.building_name = building.name
    allocs = db.query(WaterAllocation).filter(
        WaterAllocation.water_expense_id == we.id
    ).all()
    data.allocations = [_alloc_to_response(a, db) for a in allocs]
    return data


@router.get("", response_model=WaterExpenseListResponse)
def list_water_expenses(
    building_id: Optional[int] = Query(None),
    period: Optional[str] = Query(None, description="YYYY-MM"),
    db: Session = Depends(get_db),
):
    """水费账单列表"""
    query = db.query(WaterExpense)
    if building_id:
        query = query.filter(WaterExpense.building_id == building_id)
    if period:
        month = month_start(parse_date(period + "-01"))
        query = query.filter(
            and_(
                WaterExpense.period_start <= month,
                WaterExpense.period_end >= month,
            )
        )
    items = query.order_by(
        WaterExpense.period_start.desc(), WaterExpense.building_id.asc()
    ).all()
    return {
        "items": [_expense_to_response(e, db) for e in items],
        "total": len(items),
    }


@router.post("", response_model=WaterExpenseResponse)
def create_water_expense(
    data: WaterExpenseCreate, db: Session = Depends(get_db),
):
    """录入水费"""
    building = db.query(Building).filter(Building.id == data.building_id).first()
    if not building:
        raise NotFoundError(f"楼栋不存在: {data.building_id}")

    # 检查是否已存在
    existing = db.query(WaterExpense).filter(
        and_(
            WaterExpense.building_id == data.building_id,
            WaterExpense.period_start == data.period_start,
            WaterExpense.period_end == data.period_end,
        )
    ).first()
    if existing:
        # 更新
        for k, v in data.model_dump().items():
            setattr(existing, k, v)
        db.commit()
        db.refresh(existing)
        return _expense_to_response(existing, db)

    we = WaterExpense(**data.model_dump(), status="pending")
    db.add(we)
    db.commit()
    db.refresh(we)
    return _expense_to_response(we, db)


@router.put("/{water_expense_id}", response_model=WaterExpenseResponse)
def update_water_expense(
    water_expense_id: int, data: WaterExpenseUpdate, db: Session = Depends(get_db),
):
    """编辑水费"""
    we = db.query(WaterExpense).filter(WaterExpense.id == water_expense_id).first()
    if not we:
        raise NotFoundError(f"水费账单不存在: {water_expense_id}")
    update_data = data.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(we, k, v)
    db.commit()
    db.refresh(we)
    return _expense_to_response(we, db)


@router.post("/{water_expense_id}/allocate", response_model=WaterExpenseResponse)
def generate_allocation(
    water_expense_id: int, db: Session = Depends(get_db),
):
    """生成水费分摊"""
    we = db.query(WaterExpense).filter(WaterExpense.id == water_expense_id).first()
    if not we:
        raise NotFoundError(f"水费账单不存在: {water_expense_id}")
    allocate_water_expense(db, we)
    db.commit()
    db.refresh(we)
    return _expense_to_response(we, db)


@router.post("/allocate-batch")
def batch_update_allocations(
    data: AllocationBatchUpdate, db: Session = Depends(get_db),
):
    """批量调整分摊金额（自动平衡其他未调整项）"""
    # 按 water_expense_id 分组
    grouped = {}
    for item in data.items:
        alloc = db.query(WaterAllocation).filter(
            WaterAllocation.id == item.id
        ).first()
        if alloc:
            grouped.setdefault(alloc.water_expense_id, {})[alloc.id] = item.amount

    for expense_id, adjustments in grouped.items():
        rebalance_water_allocations(db, expense_id, adjustments)
    db.commit()
    return {"message": "ok", "updated_groups": len(grouped)}


@router.put("/allocation/{allocation_id}")
def update_single_allocation(
    allocation_id: int,
    amount: Decimal,
    remark: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """更新单条分摊金额"""
    alloc = update_water_allocation_amount(db, allocation_id, amount, remark)
    db.commit()
    db.refresh(alloc)
    return _alloc_to_response(alloc, db)


@router.delete("/{water_expense_id}")
def delete_water_expense(water_expense_id: int, db: Session = Depends(get_db)):
    """删除水费账单"""
    we = db.query(WaterExpense).filter(WaterExpense.id == water_expense_id).first()
    if not we:
        raise NotFoundError(f"水费账单不存在: {water_expense_id}")
    # 清除分摊
    db.query(WaterAllocation).filter(
        WaterAllocation.water_expense_id == water_expense_id
    ).delete()
    db.delete(we)
    db.commit()
    return {"message": "ok"}
