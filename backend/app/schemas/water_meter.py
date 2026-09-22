"""水费 Schema（简化版）"""
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel


class WaterMeterCreate(BaseModel):
    """创建水费记录"""
    building_id: int
    room_no: str
    month: date
    total_fee: Decimal = Decimal("0")
    remark: Optional[str] = None


class WaterMeterUpdate(BaseModel):
    """更新水费"""
    total_fee: Optional[Decimal] = None
    remark: Optional[str] = None


class WaterMeterResponse(BaseModel):
    """水费响应"""
    id: int
    building_id: int
    room_no: str
    month: date
    total_fee: Decimal
    remark: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # 关联信息
    building_no: Optional[str] = None
    room_name: Optional[str] = None
    occupants_count: int = 0

    class Config:
        from_attributes = True


class WaterMeterListResponse(BaseModel):
    items: list[WaterMeterResponse]
    total: int


class WaterMeterBatchCreate(BaseModel):
    """批量初始化水费"""
    month: str  # YYYY-MM
    building_id: Optional[int] = None
