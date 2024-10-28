import json
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from data_storage.crud import CompanyCRUD

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def ingest_companies():
    # 创建数据库连接
    engine = create_engine(DATABASE_URL)
    crud = CompanyCRUD()
    
    # 读取 JSON 文件
    with open('data_storage/data/companies.json', 'r', encoding='utf-8') as f:
        companies_data = json.load(f)
    
    # 创建会话
    with Session(engine) as session:
        for company_data in companies_data:
            # 创建 Company 实例
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
            # 保存到数据库
            company.save(session)
            print(f"Successfully inserted company: {company.name}")

if __name__ == "__main__":
    ingest_companies()
