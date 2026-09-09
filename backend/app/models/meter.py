"""电表记录 ORM 模型"""
from decimal import Decimal
from sqlalchemy import (
    Column, BigInteger, Date, Numeric, Enum, DateTime, Index, ForeignKey,
    UniqueConstraint, String,
)
from sqlalchemy.sql import func
from ..database import Base


class MeterRecord(Base):
    """电表记录表（每月每个房间一条记录）"""
    __tablename__ = "meter_records"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    room_id = Column(BigInteger, ForeignKey("rooms.id"), nullable=False)
    month = Column(Date, nullable=False, comment="结算月份（每月1号）")

    previous_reading = Column(Numeric(12, 2), default=Decimal("0"),
                              comment="上月普通电表读数")
    current_reading = Column(Numeric(12, 2), default=Decimal("0"),
                             comment="本月普通电表读数")
    total_degree = Column(Numeric(12, 2), default=Decimal("0"),
                          comment="普通用电量")

    ac_previous_reading = Column(Numeric(12, 2), default=Decimal("0"),
                                 comment="上月空调读数")
    ac_current_reading = Column(Numeric(12, 2), default=Decimal("0"),
                                comment="本月空调读数")
    ac_degree = Column(Numeric(12, 2), default=Decimal("0"),
                       comment="空调用电量")

    electricity_price = Column(Numeric(10, 4), default=Decimal("0.4900"),
                               comment="本月电价快照")
    ac_unit_price = Column(Numeric(10, 4), default=Decimal("0"),
                           comment="空调平均单价")
    total_fee = Column(Numeric(12, 2), default=Decimal("0"),
                       comment="普通电费")
    ac_fee = Column(Numeric(12, 2), default=Decimal("0"),
                    comment="空调电费")

    status = Column(Enum("normal", "abnormal", "manual", name="meter_status"),
                    default="normal", comment="正常/异常/手工")
    remark = Column(String(500), nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("room_id", "month", name="uk_room_month"),
        Index("idx_month", "month"),
        {"comment": "电表记录"},
    )
