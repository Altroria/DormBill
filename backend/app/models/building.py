"""楼栋 ORM 模型"""
from sqlalchemy import Column, BigInteger, String, DateTime, Enum, Index
from sqlalchemy.sql import func
from ..database import Base


class Building(Base):
    """楼栋表"""
    __tablename__ = "buildings"

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="主键")
    building_no = Column(String(20), nullable=False, unique=True, comment="楼栋编号")
    name = Column(String(50), nullable=True, comment="楼栋名称")
    address = Column(String(200), nullable=True, comment="地址")
    status = Column(Enum("active", "inactive", name="building_status"),
                    default="active", comment="使用中/停用")
    remark = Column(String(500), nullable=True, comment="备注")

    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(),
                        comment="更新时间")
    deleted_at = Column(DateTime, nullable=True, comment="软删除时间")

    __table_args__ = (
        Index("idx_building_no", "building_no"),
        Index("idx_status", "status"),
        {"comment": "楼栋"},
    )
