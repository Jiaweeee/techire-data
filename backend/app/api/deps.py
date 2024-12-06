from typing import Generator
from data_storage.config import create_db_engine
from sqlalchemy.orm import sessionmaker

engine = create_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 