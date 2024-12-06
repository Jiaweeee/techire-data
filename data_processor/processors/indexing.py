from .base import Processor
from data_storage.models import Job
from backend.app.services.es.client import ESClient
from data_processor.elasticsearch.mappings import JOB_MAPPING
from datetime import datetime
import logging, dotenv, os

dotenv.load_dotenv()
logger = logging.getLogger(__name__)

class DataIndexingProcessor(Processor):
    def __init__(self):
        self.es_client = ESClient()

    def setup(self):
        self.es_client.create_index(os.getenv("ES_JOB_INDEX"), JOB_MAPPING)

    def process(self, job: Job):
        if not job.analysis:
            logger.error(f"Job {job.id} has no analysis")
            return
        
        try:
            analysis = job.analysis
            # 构建文档
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
                "posted_date": self._format_date(job.posted_date),
                "is_remote": job.is_remote,
                "expired": job.expired,
                "skill_tags": analysis.skill_tags.split(',') if analysis.skill_tags else [],
                "summary": analysis.summary,
                "experience_level": analysis.experience_level if analysis.experience_level else None,
                "salary_range": {
                    "min": analysis.salary_min,
                    "max": analysis.salary_max,
                    "fixed": analysis.salary_fixed,
                    "currency": analysis.salary_currency
                }
            }
            
            # 检查文档是否存在并相应处理
            if self.es_client.exists_document(job.id):
                self.es_client.update_document(job.id, doc)
                logger.info(f"Successfully updated job {job.id} in Elasticsearch")
            else:
                self.es_client.index_document(job.id, doc)
                logger.info(f"Successfully indexed new job {job.id} to Elasticsearch")
            
        except Exception as e:
            logger.error(f"Error processing job {job.id} in Elasticsearch: {str(e)}")
            return False

    def _format_date(self, date_str):
        if not date_str:
            return None
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            return date_obj.strftime('%Y-%m-%dT%H:%M:%S')
        except Exception:
            return None