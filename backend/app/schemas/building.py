"""楼栋 Schema"""
from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field


class BuildingBase(BaseModel):
    building_no: str = Field(..., max_length=20, description="楼栋编号")
    name: Optional[str] = Field(None, max_length=50)
    address: Optional[str] = Field(None, max_length=200)
    status: str = Field("active", description="active/inactive")
    remark: Optional[str] = Field(None, max_length=500)


class BuildingCreate(BuildingBase):
    pass


class BuildingUpdate(BaseModel):
    building_no: Optional[str] = None
    name: Optional[str] = None
    address: Optional[str] = None
    status: Optional[str] = None
    remark: Optional[str] = None


class BuildingResponse(BuildingBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class BuildingListResponse(BaseModel):
    items: list[BuildingResponse]
    total: int
