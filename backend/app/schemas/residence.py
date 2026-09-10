"""入住记录 Schema"""
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field


class ResidenceBase(BaseModel):
    employee_id: int
    room_id: int
    check_in_date: date
    check_out_date: Optional[date] = None
    is_primary_payer: Optional[int] = 0
    probation_months: Optional[int] = 0
    status: str = "valid"
    remark: Optional[str] = None


class ResidenceCreate(ResidenceBase):
    pass


class ResidenceUpdate(BaseModel):
    check_out_date: Optional[date] = None
    is_primary_payer: Optional[int] = None
    probation_months: Optional[int] = None
    status: Optional[str] = None
    remark: Optional[str] = None


class BatchMoveOut(BaseModel):
    """批量搬离"""
    residence_ids: list[int]
    check_out_date: date


class BatchTransferItem(BaseModel):
    residence_id: int
    target_room_id: int


class BatchTransfer(BaseModel):
    """批量换房"""
    items: list[BatchTransferItem]
    transfer_date: date


class ResidenceResponse(ResidenceBase):
    id: int
    created_at: Optional[datetime] = None
    # 关联字段
    employee_name: Optional[str] = None
    employee_no: Optional[str] = None
    company: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    room_no: Optional[str] = None
    room_name: Optional[str] = None
    building_id: Optional[int] = None
    building_no: Optional[str] = None
    building_name: Optional[str] = None
    rent_standard: Optional[float] = None
    electricity_price: Optional[float] = None

    class Config:
        from_attributes = True


class ResidenceListResponse(BaseModel):
    items: list[ResidenceResponse]
    total: int
