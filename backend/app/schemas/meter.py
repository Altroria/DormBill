"""电表 Schema"""
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field


class MeterBase(BaseModel):
    room_id: int
    month: date
    previous_reading: Decimal = Decimal("0")
    current_reading: Decimal = Decimal("0")
    ac_previous_reading: Decimal = Decimal("0")
    ac_current_reading: Decimal = Decimal("0")
    electricity_price: Decimal = Decimal("0.4900")
    ac_unit_price: Decimal = Decimal("0")
    remark: Optional[str] = None


class MeterCreate(MeterBase):
    pass


class MeterUpdate(BaseModel):
    current_reading: Optional[Decimal] = None
    ac_current_reading: Optional[Decimal] = None
    electricity_price: Optional[Decimal] = None
    ac_unit_price: Optional[Decimal] = None
    remark: Optional[str] = None


class MeterResponse(MeterBase):
    id: int
    total_degree: Decimal
    ac_degree: Decimal
    total_fee: Decimal
    ac_fee: Decimal
    status: str
    created_at: Optional[datetime] = None
    # 关联字段
    room_no: Optional[str] = None
    room_name: Optional[str] = None
    building_no: Optional[str] = None
    meter_no: Optional[str] = None
    ac_meter_no: Optional[str] = None
    occupants_count: Optional[int] = None

    class Config:
        from_attributes = True


class MeterListResponse(BaseModel):
    items: list[MeterResponse]
    total: int


class MeterCalculateRequest(BaseModel):
    """批量计算请求"""
    month: date
    ac_unit_price: Optional[Decimal] = None
