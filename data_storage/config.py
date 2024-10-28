from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def create_db_engine(database_url=DATABASE_URL):
    return create_engine(
        database_url,
        pool_recycle=3600,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20
    )

def get_database_url():
    return DATABASE_URL