from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from search_service.app.core.config import settings
from search_service.app.api.v1.endpoints import search

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加路由
app.include_router(search.router, prefix=f"{settings.API_V1_STR}/search")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "search_service.main:app",
        host="0.0.0.0",
        port=8001,
        reload=True
    ) 