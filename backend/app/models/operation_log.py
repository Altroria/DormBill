"""操作日志 ORM 模型"""
from sqlalchemy import Column, BigInteger, String, DateTime, Index, Text
from sqlalchemy.sql import func
from ..database import Base


class OperationLog(Base):
    """操作日志表"""
    __tablename__ = "operation_logs"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    operator = Column(String(50), default="admin", comment="操作人")
    action = Column(String(100), nullable=False, comment="操作类型")
    target_type = Column(String(50), comment="操作对象类型")
    target_id = Column(BigInteger, comment="操作对象ID")
    detail = Column(Text, comment="操作详情(JSON)")

    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_operator", "operator"),
        Index("idx_created", "created_at"),
        {"comment": "操作日志"},
    )
