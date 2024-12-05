from search_service.app.services.es.client import ESClient
from search_service.app.services.es.mappings import JOB_MAPPING
from search_service.app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data_storage.models import Job
from data_storage.config import get_database_url
from datetime import datetime

def format_date(date_str):
    """格式化日期字符串为 ISO 格式"""
    if not date_str:
        return None
    try:
        # 将字符串解析为 datetime 对象
        date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        # 转换为 ISO 格式
        return date_obj.strftime('%Y-%m-%dT%H:%M:%S')
    except Exception:
        return None

def init_elasticsearch():
    """初始化 Elasticsearch 并导入数据"""
    # 创建数据库会话
    engine = create_engine(get_database_url())
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    # 创建 ES 客户端
    es_client = ESClient()
    
    try:
        # 1. 创建索引
        print("Creating index...")
        es_client.create_index(settings.ES_JOB_INDEX, JOB_MAPPING)
        
        # 2. 获取所有未过期的职位
        print("Fetching jobs from database...")
        jobs = db.query(Job).filter(Job.expired == False).all()
        
        # 3. 导入到 ES
        print(f"Importing {len(jobs)} jobs to Elasticsearch...")
        for job in jobs:
            doc = {
                "id": job.id,
                "title": job.title,
                "full_description": job.full_description,
                "company": {
                    "id": job.company.id,
                    "name": job.company.name
                },
                "location": job.location,
                "employment_type": job.employment_type,
                "posted_date": format_date(job.posted_date),
                "is_remote": job.is_remote,
                "expired": job.expired
            }
            
            # 添加分析数据
            if job.analysis:
                doc["skill_tags"] = job.analysis.skill_tags.split(',') if job.analysis.skill_tags else []
            
            es_client.index_document(job.id, doc)
            
        print("Elasticsearch initialization completed successfully!")
        
    except Exception as e:
        print(f"Error during initialization: {str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_elasticsearch() 