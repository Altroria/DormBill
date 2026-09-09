"""水费 Schema"""
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field


class WaterExpenseBase(BaseModel):
    period_start: date
    period_end: date
    building_id: int
    meter_start: Optional[Decimal] = None
    meter_end: Optional[Decimal] = None
    total_amount: Decimal = Decimal("0")
    remark: Optional[str] = None


class WaterExpenseCreate(WaterExpenseBase):
    pass


class WaterExpenseUpdate(BaseModel):
    meter_start: Optional[Decimal] = None
    meter_end: Optional[Decimal] = None
    total_amount: Optional[Decimal] = None
    remark: Optional[str] = None


class WaterExpenseResponse(WaterExpenseBase):
    id: int
    status: str
    created_at: Optional[datetime] = None
    building_no: Optional[str] = None
    building_name: Optional[str] = None
    allocations: Optional[list["WaterAllocationResponse"]] = None

    class Config:
        from_attributes = True


class WaterAllocationResponse(BaseModel):
    id: int
    water_expense_id: int
    employee_id: int
    room_id: int
    amount: Decimal
    month1_days: int
    month2_days: int
    is_valid: int
    remark: Optional[str] = None
    # 关联
    employee_name: Optional[str] = None
    employee_no: Optional[str] = None
    room_no: Optional[str] = None
    room_name: Optional[str] = None
    building_no: Optional[str] = None

    class Config:
        from_attributes = True


class WaterExpenseListResponse(BaseModel):
    items: list[WaterExpenseResponse]
    total: int


class AllocationUpdateItem(BaseModel):
    """单个分摊调整"""
    id: int
    amount: Decimal


class AllocationBatchUpdate(BaseModel):
    """批量调整分摊金额"""
    items: list[AllocationUpdateItem]


WaterExpenseResponse.model_rebuild()
