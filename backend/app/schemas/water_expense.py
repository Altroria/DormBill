"""水费账单 Schemas"""
from datetime import date
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class WaterAllocationBase(BaseModel):
    """水费分摊基础"""
    water_expense_id: int
    employee_id: int
    room_id: int
    amount: Decimal
    month1_days: int = 0
    month2_days: int = 0
    is_valid: int = 1
    remark: Optional[str] = None


class WaterAllocationCreate(WaterAllocationBase):
    """创建水费分摊"""
    pass


class WaterAllocationUpdate(BaseModel):
    """更新水费分摊"""
    amount: Optional[Decimal] = None
    is_valid: Optional[int] = None
    remark: Optional[str] = None


class WaterAllocationResponse(WaterAllocationBase):
    """水费分摊响应"""
    id: int
    employee_name: Optional[str] = None
    employee_no: Optional[str] = None
    room_no: Optional[str] = None
    room_name: Optional[str] = None
    building_no: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


class WaterExpenseBase(BaseModel):
    """水费账单基础"""
    period_start: date
    period_end: date
    building_id: int
    meter_start: Optional[Decimal] = None
    meter_end: Optional[Decimal] = None
    total_amount: Decimal
    status: str = "pending"
    remark: Optional[str] = None


class WaterExpenseCreate(WaterExpenseBase):
    """创建水费账单"""
    pass


class WaterExpenseUpdate(BaseModel):
    """更新水费账单"""
    period_start: Optional[date] = None
    period_end: Optional[date] = None
    meter_start: Optional[Decimal] = None
    meter_end: Optional[Decimal] = None
    total_amount: Optional[Decimal] = None
    status: Optional[str] = None
    remark: Optional[str] = None


class WaterExpenseResponse(WaterExpenseBase):
    """水费账单响应"""
    id: int
    created_at: Optional[date] = None
    building_no: Optional[str] = None
    building_name: Optional[str] = None
    allocations: List[WaterAllocationResponse] = []
    
    model_config = ConfigDict(from_attributes=True)


class WaterExpenseListResponse(BaseModel):
    """水费账单列表响应"""
    items: List[WaterExpenseResponse]
    total: int
