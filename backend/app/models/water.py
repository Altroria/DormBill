"""水表记录 ORM 模型"""
from decimal import Decimal
from sqlalchemy import (
    Column, BigInteger, Date, Numeric, Enum, DateTime, Index, ForeignKey,
    UniqueConstraint, String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class WaterMeterRecord(Base):
    """水费记录表（每月每个房号一条记录，直接编辑水费）"""
    __tablename__ = "water_meter_records"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    building_id = Column(BigInteger, ForeignKey("buildings.id"), nullable=False, comment="楼栋ID")
    room_no = Column(String(50), nullable=False, comment="房号（如201、247-201）")
    month = Column(Date, nullable=False, comment="结算月份（每月1号）")
    
    total_fee = Column(Numeric(12, 2), default=Decimal("0"),
                       comment="水费")

    remark = Column(String(500), nullable=True, comment="备注")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("building_id", "room_no", "month", name="uk_building_room_month"),
        Index("idx_month", "month"),
        Index("idx_building_month", "building_id", "month"),
        Index("idx_room_no", "room_no"),
        {"comment": "水费记录（按房号）"},
    )
