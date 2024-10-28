import os
from dotenv import load_dotenv
from sqlalchemy import text
from urllib.parse import urlparse
from data_storage.config import create_db_engine, get_database_url

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def create_database():
    # Parse the URL to get database name
    parsed_url = urlparse(get_database_url())
    database_name = parsed_url.path.lstrip('/')
    
    # Create engine without database name
    engine_url = f"{parsed_url.scheme}://{parsed_url.username}:{parsed_url.password}@{parsed_url.hostname}:{parsed_url.port}"
    engine = create_db_engine(engine_url)
    
    with engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {database_name}"))
        print(f"Database {database_name} created successfully")

if __name__ == "__main__":
    create_database()