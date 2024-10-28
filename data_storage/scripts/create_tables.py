import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from data_storage.models import Base

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def create_tables():
    db_file_dir = "data_storage/db"
    os.makedirs(db_file_dir, exist_ok=True)
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    create_tables()