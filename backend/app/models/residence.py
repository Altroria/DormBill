"""入住记录 ORM 模型"""
from sqlalchemy import (
    Column, BigInteger, String, Date, Integer, Enum, DateTime, Index, ForeignKey,
)
from sqlalchemy.sql import func
from ..database import Base


class ResidenceRecord(Base):
    """入住记录表"""
    __tablename__ = "residence_records"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    employee_id = Column(BigInteger, ForeignKey("employees.id"), nullable=False)
    room_id = Column(BigInteger, ForeignKey("rooms.id"), nullable=False)
    check_in_date = Column(Date, nullable=False, comment="入住日期")
    check_out_date = Column(Date, nullable=True, comment="搬离日期")
    is_primary_payer = Column(Integer, default=0, comment="是否主要缴费人(夫妻间)")
    probation_months = Column(Integer, default=0, comment="试用期月数")
    status = Column(Enum("valid", "invalid", "business_trip", "leave",
                          name="residence_status"),
                    default="valid", comment="有效/无效/出差/休假")
    remark = Column(String(500), nullable=True, comment="备注")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("idx_employee", "employee_id"),
        Index("idx_room", "room_id"),
        Index("idx_check_in", "check_in_date"),
        Index("idx_status", "status"),
        {"comment": "入住记录"},
    )
