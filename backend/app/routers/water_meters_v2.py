"""水费管理路由（简化版）"""
from datetime import date
from decimal import Decimal
from typing import Optional, List
from fastapi import APIRouter, Depends, Query, UploadFile, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from io import BytesIO

from ..database import get_db
from ..services.water_meter_v2_service import WaterMeterV2Service
from ..services.excel_service import (
    export_water_template_excel,
    import_water_from_excel,
)


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


@router.get("/export-template")
def export_water_template(
    month: str = Query(..., description="月份 YYYY-MM"),
    building_id: Optional[int] = Query(None, description="楼栋ID"),
    db: Session = Depends(get_db),
):
    """导出水费导入模板（Excel）"""
    from ..models.water import WaterMeterRecord
    from ..models.building import Building
    from sqlalchemy import and_, distinct
    from ..models.room import Room
    
    month_date = date.fromisoformat(f"{month}-01")
    
    # 查询水费记录（按房号分组）
    query = db.query(
        WaterMeterRecord.building_id,
        WaterMeterRecord.room_no,
    ).filter(
        WaterMeterRecord.month == month_date
    ).distinct()
    
    if building_id:
        query = query.filter(WaterMeterRecord.building_id == building_id)
    
    water_records = query.all()
    
    # 构建房间数据
    rooms_data = []
    for record in water_records:
        building = db.query(Building).filter(Building.id == record.building_id).first()
        
        # 获取房间名称（取第一个房间）
        room = db.query(Room).filter(
            and_(
                Room.building_id == record.building_id,
                Room.room_no == record.room_no,
                Room.status == "active"
            )
        ).first()
        
        rooms_data.append({
            "building_id": record.building_id,
            "building_no": building.building_no if building else "",
            "room_no": record.room_no,
            "room_name": room.room_name if room else "",
        })
    
    # 生成Excel
    excel_bytes = export_water_template_excel(
        month=month_date,
        building_id=building_id,
        rooms_data=rooms_data
    )
    
    filename = f"水费导入模板_{month}.xlsx"
    
    return StreamingResponse(
        BytesIO(excel_bytes),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.post("/import-excel")
async def import_water_excel(
    month: str = Query(..., description="月份 YYYY-MM"),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """从Excel导入水费数据"""
    month_date = date.fromisoformat(f"{month}-01")
    
    # 读取上传的文件
    content = await file.read()
    bio = BytesIO(content)
    
    # 解析Excel
    result = import_water_from_excel(bio, month_date)
    
    service = WaterMeterV2Service(db)
    
    success_count = 0
    import_errors = []
    
    # 导入水费数据
    for water_data in result["water_meters"]:
        try:
            service.update_water_meter(
                building_id=water_data["building_id"],
                room_no=water_data["room_no"],
                month=month_date,
                total_fee=Decimal(str(water_data["total_fee"])),
                remark=water_data.get("remark"),
            )
            success_count += 1
        except Exception as e:
            import_errors.append({
                "data": f"{water_data['building_id']}-{water_data['room_no']}",
                "error": str(e)
            })
    
    return {
        "message": f"导入完成：成功 {success_count} 条",
        "imported": success_count,
        "parse_errors": result["errors"],
        "import_errors": import_errors,
    }
