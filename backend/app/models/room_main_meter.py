"""房号总电表记录 ORM 模型"""
from decimal import Decimal
from sqlalchemy import (
    Column, BigInteger, Date, Numeric, Enum, DateTime, Index, ForeignKey,
    UniqueConstraint, String,
)
from sqlalchemy.sql import func
from ..database import Base


class RoomMainMeterRecord(Base):
    """房号总电表记录表（每月每个房号一条记录）"""
    __tablename__ = "room_main_meter_records"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    building_id = Column(BigInteger, ForeignKey("buildings.id"), nullable=False)
    room_no = Column(String(50), nullable=False, comment="房号（如201、202）")
    month = Column(Date, nullable=False, comment="结算月份（每月1号）")
    meter_no = Column(String(50), nullable=True, comment="总电表编号")

    previous_reading = Column(Numeric(12, 2), default=Decimal("0"),
                              comment="上月读数")
    current_reading = Column(Numeric(12, 2), default=Decimal("0"),
                             comment="本月读数")
    total_degree = Column(Numeric(12, 2), default=Decimal("0"),
                          comment="用电量")

    electricity_price = Column(Numeric(10, 4), default=Decimal("0.4900"),
                               comment="电价")
    total_fee = Column(Numeric(12, 2), default=Decimal("0"),
                       comment="电费")
    
    common_degree = Column(Numeric(12, 2), default=Decimal("0"),
                          comment="公共用电量（总表-空调表）")
    common_fee = Column(Numeric(12, 2), default=Decimal("0"),
                       comment="公共电费（总表电费-空调电费）")

    status = Column(Enum("pending", "recorded", "calculated", name="main_meter_status"),
                    default="pending", comment="待录入/已录入/已计算")
    remark = Column(String(500), nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("building_id", "room_no", "month", name="uk_building_room_month"),
        Index("idx_main_meter_month", "month"),
        Index("idx_main_meter_building_room", "building_id", "room_no"),
        {"comment": "房号总电表记录"},
    )
