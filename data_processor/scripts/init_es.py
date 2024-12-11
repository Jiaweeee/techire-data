from backend.app.services.es.client import ESClient
from data_processor.elasticsearch.mappings import JOB_MAPPING
from backend.app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data_storage.models import Job, JobAnalysis
from data_storage.config import get_database_url
from datetime import datetime

def format_date(date_str):
    """格式化日期字符串为 ISO 格式"""
    if not date_str:
        return None
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        return date_obj.strftime('%Y-%m-%dT%H:%M:%S')
    except Exception:
        return None

def init_elasticsearch(batch_size=1000):
    """初始化 Elasticsearch 并导入数据"""
    engine = create_engine(get_database_url())
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    es_client = ESClient()
    
    try:
        # 生成新的索引名（使用时间戳）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        index_name = f"{settings.ES_JOB_INDEX}_{timestamp}"
        
        print(f"Creating new index: {index_name}")
        es_client.create_index(index_name, JOB_MAPPING)
        
        print("Fetching and importing jobs from database...")
        offset = 0
        while True:
            # 分批查询数据
            jobs = (db.query(Job)
                   .join(JobAnalysis, Job.id == JobAnalysis.job_id)
                   .filter(Job.expired == False)
                   .filter(JobAnalysis.status == 'completed')
                   .order_by(Job.id)
                   .limit(batch_size)
                   .offset(offset)
                   .all())
            
            # 如果没有更多数据，退出循环
            if not jobs:
                break
                
            print(f"Processing batch of {len(jobs)} jobs (offset: {offset})...")
            
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
                    "expired": job.expired,
                    "skill_tags": job.analysis.skill_tags.split(',') if job.analysis.skill_tags else [],
                    "summary": job.analysis.summary,
                    "experience_level": job.analysis.experience_level if job.analysis.experience_level else None,
                    "salary_range": {
                        "min": job.analysis.salary_min,
                        "max": job.analysis.salary_max,
                        "fixed": job.analysis.salary_fixed,
                        "currency": job.analysis.salary_currency,
                        "period": job.analysis.salary_period
                    }
                }
                
                es_client.index_document(job.id, doc, index=index_name)
            
            offset += batch_size
            
        # 检查并删除旧的别名和索引
        if es_client.client.indices.exists_alias(name=settings.ES_JOB_INDEX):
            # 获取所有指向该别名的索引
            aliases = es_client.client.indices.get_alias(name=settings.ES_JOB_INDEX)
            for old_index in aliases:
                print(f"Deleting old index: {old_index}")
                es_client.delete_index(old_index)
        
        # 创建新的别名
        print(f"Creating alias {settings.ES_JOB_INDEX} for index {index_name}")
        es_client.create_alias(index_name, settings.ES_JOB_INDEX)
        
        print("Elasticsearch initialization completed successfully!")
        
    except Exception as e:
        print(f"Error during initialization: {str(e)}")
        # 清理失败的新索引
        es_client.delete_index(index_name)
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_elasticsearch(batch_size=1000) 