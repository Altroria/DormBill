"""员工 API"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from ..database import get_db
from ..models import Employee
from ..schemas.employee import (
    EmployeeCreate, EmployeeUpdate, EmployeeResponse, EmployeeListResponse,
)
from ..utils.exceptions import NotFoundError, DuplicateError


router = APIRouter()


@router.get("", response_model=EmployeeListResponse)
def list_employees(
    keyword: Optional[str] = Query(None, description="工号/姓名搜索"),
    company: Optional[str] = Query(None),
    department: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """员工列表"""
    query = db.query(Employee).filter(Employee.deleted_at.is_(None))
    if keyword:
        kw = f"%{keyword}%"
        query = query.filter(
            or_(Employee.employee_no.like(kw), Employee.name.like(kw))
        )
    if company:
        query = query.filter(Employee.company == company)
    if department:
        query = query.filter(Employee.department == department)
    if status:
        query = query.filter(Employee.status == status)
    total = query.count()
    items = (
        query.order_by(Employee.employee_no.asc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return {
        "items": [EmployeeResponse.model_validate(e) for e in items],
        "total": total,
    }


@router.post("", response_model=EmployeeResponse)
def create_employee(data: EmployeeCreate, db: Session = Depends(get_db)):
    """新增员工"""
    existing = db.query(Employee).filter(
        and_(
            Employee.employee_no == data.employee_no,
            Employee.deleted_at.is_(None),
        )
    ).first()
    if existing:
        raise DuplicateError(f"工号已存在: {data.employee_no}")
    emp = Employee(**data.model_dump())
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return EmployeeResponse.model_validate(emp)


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    """员工详情"""
    emp = db.query(Employee).filter(
        and_(Employee.id == employee_id, Employee.deleted_at.is_(None))
    ).first()
    if not emp:
        raise NotFoundError(f"员工不存在: {employee_id}")
    return EmployeeResponse.model_validate(emp)


@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int, data: EmployeeUpdate, db: Session = Depends(get_db),
):
    """编辑员工"""
    emp = db.query(Employee).filter(
        and_(Employee.id == employee_id, Employee.deleted_at.is_(None))
    ).first()
    if not emp:
        raise NotFoundError(f"员工不存在: {employee_id}")
    update_data = data.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(emp, k, v)
    db.commit()
    db.refresh(emp)
    return EmployeeResponse.model_validate(emp)


@router.delete("/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    """删除员工（软删除）"""
    emp = db.query(Employee).filter(
        and_(Employee.id == employee_id, Employee.deleted_at.is_(None))
    ).first()
    if not emp:
        raise NotFoundError(f"员工不存在: {employee_id}")
    emp.deleted_at = emp.updated_at
    db.commit()
    return {"message": "ok"}
