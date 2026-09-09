"""员工 Schema"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class EmployeeBase(BaseModel):
    employee_no: str = Field(..., max_length=30, description="工号")
    name: str = Field(..., max_length=50)
    company: Optional[str] = Field(None, max_length=50)
    department: Optional[str] = Field(None, max_length=50)
    position: Optional[str] = Field(None, max_length=50)
    status: str = "active"
    remark: Optional[str] = None


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    employee_no: Optional[str] = None
    name: Optional[str] = None
    company: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    status: Optional[str] = None
    remark: Optional[str] = None


class EmployeeResponse(EmployeeBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class EmployeeListResponse(BaseModel):
    items: list[EmployeeResponse]
    total: int
