"""自定义异常"""
from fastapi import HTTPException, status


class DormBillException(HTTPException):
    """系统自定义异常基类"""
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "系统错误"

    def __init__(self, detail: str | None = None):
        super().__init__(
            status_code=self.status_code,
            detail=detail or self.detail,
        )


class NotFoundError(DormBillException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "记录不存在"


class DuplicateError(DormBillException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "记录已存在"


class ValidationError(DormBillException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "数据校验失败"


class BusinessError(DormBillException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "业务规则冲突"


__all__ = [
    "DormBillException",
    "NotFoundError",
    "DuplicateError",
    "ValidationError",
    "BusinessError",
]
