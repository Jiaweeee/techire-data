import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from data_storage.models import Base

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def drop_tables():
    engine = create_engine(DATABASE_URL)
    Base.metadata.drop_all(engine)

if __name__ == "__main__":
    drop_tables()