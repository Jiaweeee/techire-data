from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API 配置
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Search Service"
    
    # CORS 配置
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8000"
    ]
    
    # Elasticsearch 配置
    ES_HOSTS: List[str] = ["http://localhost:9200"]
    ES_USERNAME: str = "elastic"
    ES_PASSWORD: str = "123456"
    ES_JOB_INDEX: str = "jobs"
    ES_TIMEOUT: int = 30
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "allow"

settings = Settings() 