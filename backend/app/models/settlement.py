"""月度结算 ORM 模型"""
from decimal import Decimal
from sqlalchemy import (
    Column, BigInteger, Date, Numeric, Enum, DateTime, Index, ForeignKey,
    Integer, UniqueConstraint, String,
)
from sqlalchemy.sql import func
from ..database import Base


class MonthlySettlement(Base):
    """月度结算表"""
    __tablename__ = "monthly_settlements"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    month = Column(Date, nullable=False, comment="结算月份")
    employee_id = Column(BigInteger, ForeignKey("employees.id"),
                         nullable=False)
    room_id = Column(BigInteger, ForeignKey("rooms.id"), nullable=False)

    rent_should = Column(Numeric(10, 2), default=Decimal("0"), comment="应住房租")
    rent_actual = Column(Numeric(10, 2), default=Decimal("0"), comment="实扣房租")
    stay_days = Column(Integer, default=0, comment="实际入住天数")

    electricity_fee = Column(Numeric(10, 2), default=Decimal("0"),
                             comment="个人普通电费")
    ac_electricity_fee = Column(Numeric(10, 2), default=Decimal("0"),
                                comment="个人空调电费")
    water_fee = Column(Numeric(10, 2), default=Decimal("0"),
                       comment="个人水费")

    deduction_minus = Column(Numeric(10, 2), default=Decimal("0"),
                            comment="补扣-")
    deduction_plus = Column(Numeric(10, 2), default=Decimal("0"),
                            comment="补扣+")
    total_amount = Column(Numeric(10, 2), default=Decimal("0"),
                          comment="最终扣款")

    status = Column(Enum("draft", "generated", "locked",
                          name="settlement_status"),
                    default="draft", comment="草稿/已生成/已锁定")
    remark = Column(String(500), nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("month", "employee_id", name="uk_month_employee"),
        Index("idx_month", "month"),
        Index("idx_status", "status"),
        {"comment": "月度结算"},
    )
