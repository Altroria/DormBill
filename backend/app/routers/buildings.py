"""楼栋 API"""
from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from ..database import get_db
from ..models import Building
from ..schemas.building import (
    BuildingCreate, BuildingUpdate, BuildingResponse, BuildingListResponse,
)
from ..utils.exceptions import NotFoundError, DuplicateError


router = APIRouter()


@router.get("", response_model=BuildingListResponse)
def list_buildings(
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    status: Optional[str] = Query(None, description="状态筛选"),
    db: Session = Depends(get_db),
):
    """楼栋列表"""
    query = db.query(Building).filter(Building.deleted_at.is_(None))
    if keyword:
        kw = f"%{keyword}%"
        query = query.filter(
            or_(
                Building.building_no.like(kw),
                Building.name.like(kw),
                Building.address.like(kw),
            )
        )
    if status:
        query = query.filter(Building.status == status)
    query = query.order_by(Building.building_no.asc())
    items = query.all()
    return {
        "items": [BuildingResponse.model_validate(b) for b in items],
        "total": len(items),
    }


@router.post("", response_model=BuildingResponse)
def create_building(data: BuildingCreate, db: Session = Depends(get_db)):
    """新增楼栋"""
    existing = db.query(Building).filter(
        and_(
            Building.building_no == data.building_no,
            Building.deleted_at.is_(None),
        )
    ).first()
    if existing:
        raise DuplicateError(f"楼栋编号已存在: {data.building_no}")

    building = Building(**data.model_dump())
    db.add(building)
    db.commit()
    db.refresh(building)
    return BuildingResponse.model_validate(building)


@router.get("/{building_id}", response_model=BuildingResponse)
def get_building(building_id: int, db: Session = Depends(get_db)):
    """楼栋详情"""
    building = db.query(Building).filter(
        and_(Building.id == building_id, Building.deleted_at.is_(None))
    ).first()
    if not building:
        raise NotFoundError(f"楼栋不存在: {building_id}")
    return BuildingResponse.model_validate(building)


@router.put("/{building_id}", response_model=BuildingResponse)
def update_building(
    building_id: int, data: BuildingUpdate, db: Session = Depends(get_db),
):
    """编辑楼栋"""
    building = db.query(Building).filter(
        and_(Building.id == building_id, Building.deleted_at.is_(None))
    ).first()
    if not building:
        raise NotFoundError(f"楼栋不存在: {building_id}")

    update_data = data.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(building, k, v)
    db.commit()
    db.refresh(building)
    return BuildingResponse.model_validate(building)


@router.delete("/{building_id}")
def delete_building(building_id: int, db: Session = Depends(get_db)):
    """删除楼栋（软删除）"""
    building = db.query(Building).filter(
        and_(Building.id == building_id, Building.deleted_at.is_(None))
    ).first()
    if not building:
        raise NotFoundError(f"楼栋不存在: {building_id}")
    building.deleted_at = building.updated_at
    db.commit()
    return {"message": "ok"}
