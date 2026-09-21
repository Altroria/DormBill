"""电表管理V2 Schemas（总表+空调表分离）"""
from datetime import date
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field


class AcMeterInfo(BaseModel):
    """空调表信息"""
    room_id: int
    room_unit: Optional[str] = None
    ac_meter_no: Optional[str] = None
    ac_previous_reading: float
    ac_current_reading: float
    ac_degree: float
    ac_fee: float
    occupants: int = 0


class CombinedMeterItem(BaseModel):
    """组合电表项（总表+空调表）"""
    building_id: int
    room_no: str
    month: date
    # 总表数据
    main_meter_no: Optional[str] = None
    main_previous_reading: float
    main_current_reading: float
    main_total_degree: float
    main_total_fee: float
    # 空调表数据（数组）
    ac_meters: List[AcMeterInfo]
    # 状态
    status: str
    remark: Optional[str] = None


class CombinedMeterListResponse(BaseModel):
    """组合电表列表响应"""
    items: List[CombinedMeterItem]
    total: int
    skip: int
    limit: int


class MainMeterUpdateRequest(BaseModel):
    """总表更新请求"""
    current_reading: Optional[Decimal] = None
    meter_no: Optional[str] = None
    remark: Optional[str] = None


class AcMeterUpdateRequest(BaseModel):
    """空调表更新请求"""
    room_id: int
    ac_current_reading: Optional[Decimal] = None
    ac_meter_no: Optional[str] = None


class MeterCalculateRequest(BaseModel):
    """电表计算请求"""
    building_id: Optional[int] = None
    month: Optional[str] = Field(None, description="月份 YYYY-MM")


class MeterCalculateResponse(BaseModel):
    """电表计算响应"""
    main_meters_calculated: int
    ac_meters_calculated: int


class InitMonthRequest(BaseModel):
    """初始化月度请求"""
    month: str = Field(..., description="月份 YYYY-MM")
    building_id: Optional[int] = Field(None, description="楼栋ID，不传则初始化所有楼栋")


class InitMonthResponse(BaseModel):
    """初始化月度响应"""
    main_meter_count: int
    ac_meter_count: int


class AcMeterBatchUpdateItem(BaseModel):
    """批量更新中的空调表项"""
    room_id: int
    ac_current_reading: Decimal


class RoomNoBatchUpdateItem(BaseModel):
    """批量更新中的房号项（包含总表+多个空调表）"""
    building_id: int
    room_no: str
    main_current_reading: Decimal
    main_meter_no: Optional[str] = None
    ac_meters: List[AcMeterBatchUpdateItem]


class BatchUpdateRequest(BaseModel):
    """批量更新请求"""
    month: str = Field(..., description="月份 YYYY-MM")
    updates: List[RoomNoBatchUpdateItem]


class BatchUpdateResponse(BaseModel):
    """批量更新响应"""
    main_meters_updated: int
    ac_meters_updated: int
    message: str


class EnhancedCalculateRequest(BaseModel):
    """增强的计算请求"""
    month: str = Field(..., description="月份 YYYY-MM")
    building_id: Optional[int] = None
    calculate_distribution: bool = Field(True, description="是否计算个人分摊")


class EnhancedCalculateResponse(BaseModel):
    """增强的计算响应"""
    main_meters_calculated: int
    distributions_created: int
    total_common_fee: float
    total_ac_fee: float
    total_fee: float


class EnhancedMeterListItem(BaseModel):
    """增强的电表列表项（包含统计信息）"""
    building_id: int
    building_no: Optional[str] = None
    room_no: str
    month: date
    # 总表读数
    main_previous_reading: float
    main_current_reading: float
    # 总表数据
    main_total_degree: float
    main_total_fee: float
    common_degree: float
    common_fee: float
    # 空调汇总
    total_ac_degree: float
    total_ac_fee: float
    # 套间明细
    ac_meters: List[AcMeterInfo]
    # 统计
    total_occupants: int
    common_fee_per_person: float
    status: str


class EnhancedMeterListResponse(BaseModel):
    """增强的电表列表响应"""
    items: List[EnhancedMeterListItem]
    total: int
