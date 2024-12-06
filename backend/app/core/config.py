from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API 配置
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Backend Service"
    
    # CORS 配置
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8000"
    ]
    
    # Elasticsearch 配置
    ES_HOSTS: List[str]
    ES_USERNAME: str
    ES_PASSWORD: str
    ES_JOB_INDEX: str
    ES_TIMEOUT: int
    ES_MAX_RETRIES: int = 3
    ES_MAX_CONNECTIONS: int = 100
    ES_RETRY_ON_TIMEOUT: bool = True
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "allow"

settings = Settings() 