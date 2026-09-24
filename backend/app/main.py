"""FastAPI 应用入口"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import traceback
import logging

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from .config import settings
from .database import init_db
from .routers import (
    buildings, rooms, employees, residences,
    meters, settlements, export, dashboard, import_data,
    water_expenses,
)
from .routers.meters_v2 import router as meters_v2_router
from .routers.water_meters_v2 import router as water_meters_v2_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="行政宿舍管理系统 API",
        description="宿舍房租、水电费用管理系统",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 全局异常处理器
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"请求异常: {request.url}")
        logger.error(f"异常类型: {type(exc).__name__}")
        logger.error(f"异常信息: {str(exc)}")
        logger.error(f"异常堆栈:\n{traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={"detail": str(exc), "type": type(exc).__name__}
        )

    # 注册路由
    app.include_router(dashboard.router, prefix="/api", tags=["首页"])
    app.include_router(buildings.router, prefix="/api/buildings", tags=["楼栋"])
    app.include_router(rooms.router, prefix="/api/rooms", tags=["房间"])
    app.include_router(employees.router, prefix="/api/employees", tags=["员工"])
    app.include_router(residences.router, prefix="/api/residences", tags=["入住"])
    app.include_router(meters.router, prefix="/api/meters", tags=["电表（旧版）"])
    app.include_router(meters_v2_router, prefix="/api", tags=["电表管理V2"])
    app.include_router(water_meters_v2_router, prefix="/api", tags=["水表管理V2"])
    app.include_router(water_expenses.router, prefix="/api/water-expenses", tags=["水费账单（旧版）"])
    app.include_router(settlements.router, prefix="/api/settlements", tags=["结算"])
    app.include_router(export.router, prefix="/api/export", tags=["导出"])
    app.include_router(import_data.router, prefix="/api/import", tags=["导入"])

    @app.on_event("startup")
    def on_startup():
        """启动事件 - 初始化数据库"""
        try:
            init_db()
        except Exception as e:
            print(f"[WARNING] 数据库初始化失败: {e}")
            print("请检查 .env 配置和 MySQL 服务是否运行")

    @app.get("/", tags=["健康检查"])
    def root():
        return {
            "name": "行政宿舍管理系统 API",
            "version": "1.0.0",
            "status": "running",
        }

    @app.get("/health", tags=["健康检查"])
    def health():
        return {"status": "ok"}

    return app


app = create_app()
