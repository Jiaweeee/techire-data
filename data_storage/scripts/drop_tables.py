from data_storage.models import Base
from data_storage.config import create_db_engine

def drop_tables():
    engine = create_db_engine()
    Base.metadata.drop_all(engine)

if __name__ == "__main__":
    drop_tables()