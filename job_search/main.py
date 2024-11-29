import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .api.v1.router import api_router

def create_app() -> FastAPI:
    """
    创建 FastAPI 应用
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )

    # Set CORS middleware
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Include API router
    app.include_router(api_router, prefix=settings.API_V1_STR)
    
    return app

app = create_app()

if __name__ == "__main__":
    """
    生产环境使用命令:
    gunicorn job_search.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
    
    开发环境使用命令:
    python -m job_search.main
    """
    uvicorn.run(
        "job_search.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # 开发模式下启用热重载
    ) 