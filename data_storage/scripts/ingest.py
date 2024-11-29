import json
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from data_storage.crud import CompanyCRUD
from data_storage.models import Base
from data_storage.config import create_db_engine

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def create_tables():
    engine = create_db_engine()
    Base.metadata.create_all(engine)

def ingest_companies():
    crud = CompanyCRUD()
    
    # 读取 JSON 文件
    with open('data_storage/configs/companies.json', 'r', encoding='utf-8') as f:
        companies_data = json.load(f)
    
    for company_data in companies_data:
        # if company already exists, update it  
        company = crud.get_by_code(company_data['code'])
        if company:
            crud.update(company.id, **company_data)
        else:
            # Create new company
            company = crud.create(
                code=company_data['code'],
                name=company_data['name'],
                official_site_url=company_data['official_site_url'],
                careers_page_url=company_data['careers_page_url'],
                icon_url=company_data['icon_url'],
                introduction=company_data['introduction'],
                industry=company_data['industry'],
                headquarters=company_data['headquarters']
            )
        print(f"Successfully inserted company: {company.name}")

if __name__ == "__main__":
    create_tables()
    ingest_companies()