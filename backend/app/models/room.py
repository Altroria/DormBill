"""房间 ORM 模型"""
from decimal import Decimal
from sqlalchemy import (
    Column, BigInteger, String, Numeric, Enum, DateTime, Index,
    ForeignKey, UniqueConstraint,
)
from sqlalchemy.sql import func

from ..database import Base


class Room(Base):
    """房间表（一个宿舍 = 一条房间记录）"""
    __tablename__ = "rooms"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    building_id = Column(BigInteger, ForeignKey("buildings.id"), nullable=False)
    room_no = Column(String(20), nullable=False, comment="房号")
    room_unit = Column(String(20), nullable=True, comment="室号")
    room_name = Column(String(50), nullable=False, comment="房间名称")
    meter_no = Column(String(50), nullable=True, comment="电表编号")
    ac_meter_no = Column(String(50), nullable=True, comment="空调电表编号")
    electricity_price = Column(Numeric(10, 4), default=Decimal("0.4900"),
                               comment="默认电价")
    rent_standard = Column(Numeric(10, 2), default=Decimal("0.00"),
                           comment="房租标准")
    status = Column(Enum("active", "inactive", name="room_status"),
                    default="active")
    remark = Column(String(500), nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    __table_args__ = (
        Index("idx_building_room", "building_id", "room_no"),
        Index("idx_room_name", "room_name"),
        UniqueConstraint("building_id", "room_no", "room_name",
                         name="uk_building_room_name"),
        {"comment": "房间(宿舍)"},
    )
