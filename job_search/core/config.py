from pydantic_settings import BaseSettings
from data_storage.config import get_database_url

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Job Search API"
    
    # CORS Origins
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173"
    ]
    
    # Database
    DATABASE_URL: str = get_database_url()
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 