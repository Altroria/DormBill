"""水费账单模型"""
from datetime import date
from decimal import Decimal
from sqlalchemy import Column, Integer, BigInteger, String, Numeric, Date, ForeignKey, Index
from sqlalchemy.orm import relationship
from ..database import Base


class WaterExpense(Base):
    """水费账单 - 按楼栋统计的水费"""
    __tablename__ = "water_expenses"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    period_start = Column(Date, nullable=False, comment="账单开始日期")
    period_end = Column(Date, nullable=False, comment="账单结束日期")
    building_id = Column(BigInteger, ForeignKey("buildings.id"), nullable=False, comment="楼栋ID")
    meter_start = Column(Numeric(10, 2), comment="起始读数")
    meter_end = Column(Numeric(10, 2), comment="结束读数")
    total_amount = Column(Numeric(10, 2), nullable=False, default=0, comment="总金额")
    status = Column(
        String(20), 
        nullable=False, 
        default="pending",
        comment="状态: pending-待分摊, allocated-已分摊, settled-已结算"
    )
    remark = Column(String(500), comment="备注")
    created_at = Column(Date, nullable=False, default=date.today, comment="创建时间")
    
    # 关联
    building = relationship("Building", back_populates="water_expenses")
    allocations = relationship("WaterAllocation", back_populates="water_expense", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index("idx_water_expense_building_period", "building_id", "period_start", "period_end"),
    )


class WaterAllocation(Base):
    """水费分摊记录"""
    __tablename__ = "water_allocations"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    water_expense_id = Column(Integer, ForeignKey("water_expenses.id"), nullable=False, comment="水费账单ID")
    employee_id = Column(BigInteger, ForeignKey("employees.id"), nullable=False, comment="员工ID")
    room_id = Column(BigInteger, ForeignKey("rooms.id"), nullable=False, comment="房间ID")
    amount = Column(Numeric(10, 2), nullable=False, default=0, comment="分摊金额")
    month1_days = Column(Integer, nullable=False, default=0, comment="第一个月天数")
    month2_days = Column(Integer, nullable=False, default=0, comment="第二个月天数")
    is_valid = Column(Integer, nullable=False, default=1, comment="是否有效: 1-有效, 0-无效")
    remark = Column(String(500), comment="备注")
    
    # 关联
    water_expense = relationship("WaterExpense", back_populates="allocations")
    employee = relationship("Employee")
    room = relationship("Room")
    
    __table_args__ = (
        Index("idx_water_alloc_expense", "water_expense_id"),
        Index("idx_water_alloc_employee", "employee_id"),
    )
