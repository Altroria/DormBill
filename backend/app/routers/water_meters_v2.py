"""水费管理路由（简化版）"""
from datetime import date
from decimal import Decimal
from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..database import get_db
from ..services.water_meter_v2_service import WaterMeterV2Service


router = APIRouter(prefix="/water-meters-v2", tags=["水费管理"])


# ========== Schemas ==========

class InitMonthRequest(BaseModel):
    month: str  # YYYY-MM
    building_id: Optional[int] = None


class InitMonthResponse(BaseModel):
    water_meter_count: int
    message: str


class WaterMeterItem(BaseModel):
    id: int
    room_no: str
    building_id: int
    building_no: str
    room_name: Optional[str]
    month: date
    total_fee: float
    remark: Optional[str]
    occupants_count: int


class WaterMeterListResponse(BaseModel):
    items: List[WaterMeterItem]
    total: int


class WaterMeterUpdateRequest(BaseModel):
    total_fee: Optional[float] = None
    remark: Optional[str] = None


class BatchUpdateItem(BaseModel):
    building_id: int
    room_no: str
    total_fee: Optional[float] = None
    remark: Optional[str] = None


class BatchUpdateRequest(BaseModel):
    month: str  # YYYY-MM
    updates: List[BatchUpdateItem]


class BatchUpdateResponse(BaseModel):
    updated_count: int
    message: str


# ========== Routes ==========

@router.post("/init-month", response_model=InitMonthResponse)
def init_month(
    data: InitMonthRequest,
    db: Session = Depends(get_db),
):
    """初始化月度水费记录"""
    service = WaterMeterV2Service(db)
    
    month_date = date.fromisoformat(f"{data.month}-01")
    
    result = service.init_month(
        month=month_date,
        building_id=data.building_id,
    )
    
    return result


@router.get("/list", response_model=WaterMeterListResponse)
def get_water_meter_list(
    month: str = Query(..., description="月份 YYYY-MM"),
    building_id: Optional[int] = Query(None, description="楼栋ID"),
    room_no: Optional[str] = Query(None, description="房号（模糊查询）"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """获取水费列表"""
    service = WaterMeterV2Service(db)
    
    month_date = date.fromisoformat(f"{month}-01")
    
    result = service.get_water_meter_list(
        month=month_date,
        building_id=building_id,
        room_no=room_no,
        skip=skip,
        limit=limit,
    )
    
    return result


@router.put("/{building_id}/{room_no}/{month}")
def update_water_meter(
    building_id: int,
    room_no: str,
    month: str,
    data: WaterMeterUpdateRequest,
    db: Session = Depends(get_db),
):
    """更新单个水费"""
    service = WaterMeterV2Service(db)
    
    month_date = date.fromisoformat(f"{month}-01")
    
    record = service.update_water_meter(
        building_id=building_id,
        room_no=room_no,
        month=month_date,
        total_fee=Decimal(str(data.total_fee)) if data.total_fee is not None else None,
        remark=data.remark,
    )
    
    return {
        "id": record.id,
        "building_id": record.building_id,
        "room_no": record.room_no,
        "month": record.month,
        "total_fee": float(record.total_fee),
        "remark": record.remark,
    }


@router.post("/batch-update", response_model=BatchUpdateResponse)
def batch_update_water_meters(
    data: BatchUpdateRequest,
    db: Session = Depends(get_db),
):
    """批量更新水费"""
    service = WaterMeterV2Service(db)
    
    month_date = date.fromisoformat(f"{data.month}-01")
    
    updates = []
    for item in data.updates:
        update_dict = {
            "building_id": item.building_id,
            "room_no": item.room_no,
        }
        if item.total_fee is not None:
            update_dict["total_fee"] = Decimal(str(item.total_fee))
        if item.remark is not None:
            update_dict["remark"] = item.remark
        
        updates.append(update_dict)
    
    result = service.batch_update_water_meters(
        month=month_date,
        updates=updates,
    )
    
    return result
