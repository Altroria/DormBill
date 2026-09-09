"""结算 Schema"""
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field


class SettlementBase(BaseModel):
    month: date
    employee_id: int
    room_id: int
    rent_should: Decimal = Decimal("0")
    rent_actual: Decimal = Decimal("0")
    stay_days: int = 0
    electricity_fee: Decimal = Decimal("0")
    ac_electricity_fee: Decimal = Decimal("0")
    water_fee: Decimal = Decimal("0")
    deduction_minus: Decimal = Decimal("0")
    deduction_plus: Decimal = Decimal("0")
    total_amount: Decimal = Decimal("0")
    remark: Optional[str] = None


class SettlementUpdate(BaseModel):
    rent_actual: Optional[Decimal] = None
    deduction_minus: Optional[Decimal] = None
    deduction_plus: Optional[Decimal] = None
    remark: Optional[str] = None


class SettlementResponse(SettlementBase):
    id: int
    status: str
    created_at: Optional[datetime] = None
    # 关联
    employee_name: Optional[str] = None
    employee_no: Optional[str] = None
    company: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    room_no: Optional[str] = None
    room_name: Optional[str] = None
    building_id: Optional[int] = None
    building_no: Optional[str] = None
    room_status: Optional[str] = None

    class Config:
        from_attributes = True


class SettlementListResponse(BaseModel):
    items: list[SettlementResponse]
    total: int


class SettlementGenerateRequest(BaseModel):
    """生成结算请求"""
    month: date
    force: bool = False  # 强制覆盖已生成


class PrecheckItem(BaseModel):
    type: str  # error/warning
    message: str
    ref_type: Optional[str] = None
    ref_id: Optional[int] = None


class PrecheckResponse(BaseModel):
    blocking: list[PrecheckItem]
    warnings: list[PrecheckItem]


class LockRequest(BaseModel):
    month: date
