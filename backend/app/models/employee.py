"""员工 ORM 模型"""
from sqlalchemy import Column, BigInteger, String, Enum, DateTime, Index
from sqlalchemy.sql import func
from ..database import Base


class Employee(Base):
    """员工表"""
    __tablename__ = "employees"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    employee_no = Column(String(30), nullable=False, unique=True, comment="工号")
    name = Column(String(50), nullable=False, comment="姓名")
    company = Column(String(50), nullable=True, comment="任职单位")
    department = Column(String(50), nullable=True, comment="一级部门")
    position = Column(String(50), nullable=True, comment="职务")
    status = Column(Enum("active", "inactive", name="employee_status"),
                    default="active", comment="在职/离职")
    remark = Column(String(500), nullable=True, comment="备注")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    __table_args__ = (
        Index("idx_employee_no", "employee_no"),
        Index("idx_name", "name"),
        Index("idx_company_dept", "company", "department"),
        {"comment": "员工"},
    )
