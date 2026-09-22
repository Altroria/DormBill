"""水费账单 API"""
from typing import Optional
from datetime import date
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from ..database import get_db
from ..models import WaterExpense, WaterAllocation, Building, Room, Employee, ResidenceRecord
from ..schemas.water_expense import (
    WaterExpenseCreate, WaterExpenseUpdate, WaterExpenseResponse, WaterExpenseListResponse,
    WaterAllocationUpdate,
)
from ..utils.exceptions import NotFoundError
from ..utils.date_utils import parse_date, month_start, month_end


router = APIRouter()


def _to_response(expense: WaterExpense, db: Session) -> WaterExpenseResponse:
    """转换为响应格式"""
    data = WaterExpenseResponse.model_validate(expense)
    
    # 获取楼栋信息
    if expense.building_id:
        building = db.query(Building).filter(Building.id == expense.building_id).first()
        if building:
            data.building_no = building.building_no
            data.building_name = building.name
    
    # 获取分摊信息
    allocations = db.query(WaterAllocation, Employee, Room, Building).join(
        Employee, WaterAllocation.employee_id == Employee.id
    ).join(
        Room, WaterAllocation.room_id == Room.id
    ).join(
        Building, Room.building_id == Building.id
    ).filter(
        WaterAllocation.water_expense_id == expense.id
    ).all()
    
    data.allocations = []
    for alloc, emp, room, bldg in allocations:
        alloc_data = {
            "id": alloc.id,
            "water_expense_id": alloc.water_expense_id,
            "employee_id": alloc.employee_id,
            "room_id": alloc.room_id,
            "amount": alloc.amount,
            "month1_days": alloc.month1_days,
            "month2_days": alloc.month2_days,
            "is_valid": alloc.is_valid,
            "remark": alloc.remark,
            "employee_name": emp.name,
            "employee_no": emp.employee_no,
            "room_no": room.room_no,
            "room_name": room.room_name,
            "building_no": bldg.building_no,
        }
        from ..schemas.water_expense import WaterAllocationResponse
        data.allocations.append(WaterAllocationResponse(**alloc_data))
    
    return data


@router.get("/", response_model=WaterExpenseListResponse)
def list_water_expenses(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    building_id: Optional[int] = Query(None),
    period: Optional[str] = Query(None, description="YYYY-MM"),
    db: Session = Depends(get_db),
):
    """水费账单列表"""
    query = db.query(WaterExpense)
    
    if building_id:
        query = query.filter(WaterExpense.building_id == building_id)
    
    if period:
        # 查询账单期间与指定月份有交集的记录
        target_date = parse_date(period + "-01")
        month_start_date = month_start(target_date)
        month_end_date = month_end(target_date)
        query = query.filter(
            and_(
                WaterExpense.period_start <= month_end_date,
                WaterExpense.period_end >= month_start_date,
            )
        )
    
    total = query.count()
    expenses = query.order_by(WaterExpense.period_start.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    items = [_to_response(expense, db) for expense in expenses]
    
    return {"items": items, "total": total}


@router.post("/", response_model=WaterExpenseResponse)
def create_water_expense(
    data: WaterExpenseCreate,
    db: Session = Depends(get_db),
):
    """创建水费账单"""
    # 检查楼栋是否存在
    building = db.query(Building).filter(Building.id == data.building_id).first()
    if not building:
        raise NotFoundError(f"楼栋不存在: {data.building_id}")
    
    expense = WaterExpense(**data.model_dump())
    db.add(expense)
    db.commit()
    db.refresh(expense)
    
    return _to_response(expense, db)


@router.put("/{expense_id}", response_model=WaterExpenseResponse)
def update_water_expense(
    expense_id: int,
    data: WaterExpenseUpdate,
    db: Session = Depends(get_db),
):
    """更新水费账单"""
    expense = db.query(WaterExpense).filter(WaterExpense.id == expense_id).first()
    if not expense:
        raise NotFoundError(f"水费账单不存在: {expense_id}")
    
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(expense, key, value)
    
    db.commit()
    db.refresh(expense)
    
    return _to_response(expense, db)


@router.post("/{expense_id}/allocate", response_model=WaterExpenseResponse)
def allocate_water_expense(
    expense_id: int,
    db: Session = Depends(get_db),
):
    """自动分摊水费到各房间"""
    expense = db.query(WaterExpense).filter(WaterExpense.id == expense_id).first()
    if not expense:
        raise NotFoundError(f"水费账单不存在: {expense_id}")
    
    # 删除旧的分摊记录
    db.query(WaterAllocation).filter(WaterAllocation.water_expense_id == expense_id).delete()
    
    # 获取该楼栋的所有房间
    rooms = db.query(Room).filter(Room.building_id == expense.building_id).all()
    
    if not rooms:
        raise HTTPException(status_code=400, detail="该楼栋没有房间")
    
    # 计算总天数(用于分摊)
    period_days = (expense.period_end - expense.period_start).days + 1
    
    # 为每个房间的每个住户创建分摊记录
    allocations = []
    for room in rooms:
        # 查找在账单期间内的住户
        residents = db.query(ResidenceRecord).filter(
            and_(
                ResidenceRecord.room_id == room.id,
                ResidenceRecord.status != "invalid",
                ResidenceRecord.check_in_date <= expense.period_end,
                or_(
                    ResidenceRecord.check_out_date.is_(None),
                    ResidenceRecord.check_out_date >= expense.period_start,
                ),
            )
        ).all()
        
        for resident in residents:
            # 计算实际入住天数
            actual_start = max(resident.check_in_date, expense.period_start)
            actual_end = min(
                resident.check_out_date if resident.check_out_date else expense.period_end,
                expense.period_end
            )
            days = (actual_end - actual_start).days + 1
            
            allocations.append({
                "resident": resident,
                "room": room,
                "days": days,
            })
    
    # 按天数比例分摊
    total_days = sum(a["days"] for a in allocations)
    
    if total_days == 0:
        raise HTTPException(status_code=400, detail="账单期间内没有住户")
    
    allocated_total = 0
    for i, alloc_data in enumerate(allocations):
        days = alloc_data["days"]
        resident = alloc_data["resident"]
        room = alloc_data["room"]
        
        # 最后一个使用余额，其他按比例
        if i == len(allocations) - 1:
            amount = expense.total_amount - allocated_total
        else:
            amount = round(expense.total_amount * days / total_days, 2)
            allocated_total += amount
        
        allocation = WaterAllocation(
            water_expense_id=expense_id,
            employee_id=resident.employee_id,
            room_id=resident.room_id,
            amount=amount,
            month1_days=days,  # 简化处理，实际可能跨月
            month2_days=0,
            is_valid=1,
        )
        db.add(allocation)
    
    # 更新状态
    expense.status = "allocated"
    db.commit()
    db.refresh(expense)
    
    return _to_response(expense, db)


@router.delete("/{expense_id}")
def delete_water_expense(
    expense_id: int,
    db: Session = Depends(get_db),
):
    """删除水费账单"""
    expense = db.query(WaterExpense).filter(WaterExpense.id == expense_id).first()
    if not expense:
        raise NotFoundError(f"水费账单不存在: {expense_id}")
    
    db.delete(expense)
    db.commit()
    
    return {"message": "ok"}


@router.put("/allocation/{allocation_id}")
def update_water_allocation(
    allocation_id: int,
    amount: float = Query(...),
    remark: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """更新单个水费分摊记录"""
    allocation = db.query(WaterAllocation).filter(WaterAllocation.id == allocation_id).first()
    if not allocation:
        raise NotFoundError(f"水费分摊记录不存在: {allocation_id}")
    
    allocation.amount = amount
    if remark is not None:
        allocation.remark = remark
    
    db.commit()
    
    return {"message": "ok"}


@router.post("/allocate-batch")
def batch_update_allocations(
    items: list,
    db: Session = Depends(get_db),
):
    """批量更新水费分摊金额"""
    for item in items:
        allocation_id = item.get("id")
        amount = item.get("amount")
        
        allocation = db.query(WaterAllocation).filter(WaterAllocation.id == allocation_id).first()
        if allocation:
            allocation.amount = amount
    
    db.commit()
    
    return {"message": "ok"}
