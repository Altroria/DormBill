"""房间 Schema"""
from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field


class RoomBase(BaseModel):
    building_id: int
    room_no: str = Field(..., max_length=20)
    room_name: str = Field(..., max_length=50)
    meter_no: Optional[str] = Field(None, max_length=50)
    ac_meter_no: Optional[str] = Field(None, max_length=50)
    electricity_price: Optional[Decimal] = Field(Decimal("0.4900"), max_digits=10, decimal_places=4)
    rent_standard: Optional[Decimal] = Field(Decimal("0.00"), max_digits=10, decimal_places=2)
    status: str = "active"
    remark: Optional[str] = None


class RoomCreate(RoomBase):
    pass


class RoomBatchCreate(BaseModel):
    """批量创建房间"""
    building_id: int
    items: list[RoomBase]


class RoomUpdate(BaseModel):
    room_no: Optional[str] = None
    room_name: Optional[str] = None
    meter_no: Optional[str] = None
    ac_meter_no: Optional[str] = None
    electricity_price: Optional[Decimal] = None
    rent_standard: Optional[Decimal] = None
    status: Optional[str] = None
    remark: Optional[str] = None


class RoomResponse(RoomBase):
    id: int
    created_at: Optional[datetime] = None
    building_no: Optional[str] = None
    building_name: Optional[str] = None

    class Config:
        from_attributes = True


class RoomListResponse(BaseModel):
    items: list[RoomResponse]
    total: int
