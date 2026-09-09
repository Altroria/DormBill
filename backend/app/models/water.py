"""水费相关 ORM 模型"""
from decimal import Decimal
from sqlalchemy import (
    Column, BigInteger, Date, Numeric, Enum, DateTime, Index, ForeignKey,
    Integer, UniqueConstraint, String,
)
from sqlalchemy.sql import func
from ..database import Base


class WaterExpense(Base):
    """水费账单表（每楼栋每水费周期一条）"""
    __tablename__ = "water_expenses"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    period_start = Column(Date, nullable=False, comment="周期起始月")
    period_end = Column(Date, nullable=False, comment="周期结束月")
    building_id = Column(BigInteger, ForeignKey("buildings.id"), nullable=False)
    meter_start = Column(Numeric(12, 2), nullable=True, comment="水表起始读数")
    meter_end = Column(Numeric(12, 2), nullable=True, comment="水表截止读数")
    total_amount = Column(Numeric(12, 2), default=Decimal("0"),
                          comment="水费金额")
    status = Column(Enum("pending", "allocated", "settled", name="water_status"),
                    default="pending", comment="未录入/已分摊/已结算")
    remark = Column(String(500), nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("building_id", "period_start", "period_end",
                         name="uk_building_period"),
        Index("idx_period", "period_start", "period_end"),
        {"comment": "水费账单"},
    )


class WaterAllocation(Base):
    """水费分摊表"""
    __tablename__ = "water_allocations"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    water_expense_id = Column(BigInteger, ForeignKey("water_expenses.id"),
                              nullable=False)
    employee_id = Column(BigInteger, ForeignKey("employees.id"),
                         nullable=False)
    room_id = Column(BigInteger, ForeignKey("rooms.id"), nullable=False)
    amount = Column(Numeric(10, 2), default=Decimal("0"), comment="个人水费")
    month1_days = Column(Integer, default=0, comment="第一个月有效天数")
    month2_days = Column(Integer, default=0, comment="第二个月有效天数")
    is_valid = Column(Integer, default=1, comment="是否参与分摊")
    remark = Column(String(500), nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("idx_expense", "water_expense_id"),
        Index("idx_employee", "employee_id"),
        {"comment": "水费分摊"},
    )
