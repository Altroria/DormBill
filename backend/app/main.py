"""FastAPI 应用入口"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import settings
from .database import init_db
from .routers import (
    buildings, rooms, employees, residences,
    meters, water, settlements, export, dashboard, import_data,
)


def create_app() -> FastAPI:
    app = FastAPI(
        title="蓉蓉的收租小工具 API",
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

    # 注册路由
    app.include_router(dashboard.router, prefix="/api", tags=["首页"])
    app.include_router(buildings.router, prefix="/api/buildings", tags=["楼栋"])
    app.include_router(rooms.router, prefix="/api/rooms", tags=["房间"])
    app.include_router(employees.router, prefix="/api/employees", tags=["员工"])
    app.include_router(residences.router, prefix="/api/residences", tags=["入住"])
    app.include_router(meters.router, prefix="/api/meters", tags=["电表"])
    app.include_router(water.router, prefix="/api/water-expenses", tags=["水费"])
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
            "name": "蓉蓉的收租小工具 API",
            "version": "1.0.0",
            "status": "running",
        }

    @app.get("/health", tags=["健康检查"])
    def health():
        return {"status": "ok"}

    return app


app = create_app()
