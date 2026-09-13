"""房号总电表 Schema"""
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel


class RoomMainMeterBase(BaseModel):
    building_id: int
    room_no: str
    month: date
    meter_no: Optional[str] = None
    previous_reading: Decimal = Decimal("0")
    current_reading: Decimal = Decimal("0")
    electricity_price: Decimal = Decimal("0.4900")
    remark: Optional[str] = None


class RoomMainMeterCreate(RoomMainMeterBase):
    pass


class RoomMainMeterUpdate(BaseModel):
    previous_reading: Optional[Decimal] = None  # 首次录入时可修改
    current_reading: Optional[Decimal] = None
    electricity_price: Optional[Decimal] = None
    meter_no: Optional[str] = None
    remark: Optional[str] = None


class RoomMainMeterResponse(RoomMainMeterBase):
    id: int
    total_degree: Decimal
    total_fee: Decimal
    status: str
    created_at: Optional[datetime] = None
    # 关联字段
    building_no: Optional[str] = None
    
    class Config:
        from_attributes = True


class RoomMainMeterListResponse(BaseModel):
    items: list[RoomMainMeterResponse]
    total: int


class AcMeterUpdate(BaseModel):
    """空调电表更新（单独的schema）"""
    ac_previous_reading: Optional[Decimal] = None
    ac_current_reading: Optional[Decimal] = None
    ac_unit_price: Optional[Decimal] = None
    remark: Optional[str] = None


class AcMeterResponse(BaseModel):
    """空调电表响应"""
    id: int
    room_id: int
    month: date
    ac_previous_reading: Decimal
    ac_current_reading: Decimal
    ac_degree: Decimal
    ac_unit_price: Decimal
    ac_fee: Decimal
    status: str
    remark: Optional[str] = None
    created_at: Optional[datetime] = None
    # 关联字段
    building_no: Optional[str] = None
    room_no: Optional[str] = None
    room_name: Optional[str] = None
    ac_meter_no: Optional[str] = None
    occupants_count: Optional[int] = None
    
    class Config:
        from_attributes = True


class AcMeterListResponse(BaseModel):
    items: list[AcMeterResponse]
    total: int


class CombinedMeterResponse(BaseModel):
    """组合的电表响应（总表+空调表）"""
    # 房号信息
    building_id: int
    building_no: str
    room_no: str
    month: date
    
    # 总电表
    main_meter_id: Optional[int] = None
    main_meter_no: Optional[str] = None
    main_previous_reading: Decimal = Decimal("0")
    main_current_reading: Decimal = Decimal("0")
    main_total_degree: Decimal = Decimal("0")
    main_electricity_price: Decimal = Decimal("0.4900")
    main_total_fee: Decimal = Decimal("0")
    main_status: str = "pending"
    
    # 空调电表列表（该房号下所有小房间）
    ac_meters: list[AcMeterResponse] = []
    
    # 汇总
    total_ac_fee: Decimal = Decimal("0")  # 该房号所有空调电费合计
    grand_total: Decimal = Decimal("0")   # 总电费+空调电费合计


class CombinedMeterListResponse(BaseModel):
    items: list[CombinedMeterResponse]
    total: int


class MeterCalculateRequest(BaseModel):
    """批量计算请求"""
    month: str  # YYYY-MM
    ac_unit_price: Optional[Decimal] = None
