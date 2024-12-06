from backend.app.services.es.client import ESClient
from data_processor.elasticsearch.mappings import JOB_MAPPING
from backend.app.core.config import settings
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
    engine = create_engine(get_database_url())
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    es_client = ESClient()
    
    try:
        print("Creating index...")
        es_client.create_index(settings.ES_JOB_INDEX, JOB_MAPPING)
        
        print("Fetching jobs from database...")
        jobs = db.query(Job).filter(Job.expired == False).all()
        
        print(f"Importing {len(jobs)} jobs to Elasticsearch...")
        for job in jobs:
            # 构建基础文档
            doc = {
                "id": job.id,
                "title": job.title,
                "full_description": job.full_description,
                "url": job.url,
                "company": {
                    "id": job.company.id,
                    "name": job.company.name,
                    "icon_url": job.company.icon_url
                },
                "location": job.location,
                "employment_type": job.employment_type,
                "posted_date": format_date(job.posted_date),
                "is_remote": job.is_remote,
                "expired": job.expired
            }
            
            # 添加分析数据
            if job.analysis:
                doc.update({
                    "skill_tags": job.analysis.skill_tags.split(',') if job.analysis.skill_tags else [],
                    "summary": job.analysis.summary,
                    "experience_level": job.analysis.experience_level if job.analysis.experience_level else None,
                    "salary_range": {
                        "min": job.analysis.salary_min,
                        "max": job.analysis.salary_max,
                        "fixed": job.analysis.salary_fixed,
                        "currency": job.analysis.salary_currency
                    }
                })
            
            es_client.index_document(job.id, doc)
            
        print("Elasticsearch initialization completed successfully!")
        
    except Exception as e:
        print(f"Error during initialization: {str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_elasticsearch() 