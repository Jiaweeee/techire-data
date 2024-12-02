import logging
from sqlalchemy.orm import Session
from data_storage.config import create_db_engine
from data_storage.models import Job, JobAnalysis
from .analyzer import JobAnalyzer
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JobAnalysisService:
    def __init__(self):
        self.engine = create_db_engine()
        self.analyzer = JobAnalyzer()
        
    def get_pending_jobs(self, session: Session, batch_size: int = 10):
        """获取待分析的工作"""
        # 查找 JobAnalysis 状态为 pending 的工作
        return (
            session.query(Job)
            .join(JobAnalysis)
            .filter(JobAnalysis.status.in_(['pending', 'failed']))
            .limit(batch_size)
            .all()
        )
    
    def analyze_job(self, session: Session, job: Job):
        """分析单个工作"""
        try:
            # 创建或获取分析记录
            analysis = session.query(JobAnalysis).filter_by(job_id=job.id).first()
            if not analysis:
                analysis = JobAnalysis(job_id=job.id)
                session.add(analysis)
            
            # 更新状态为处理中
            analysis.status = 'processing'
            session.commit()
            
            # 获取分析结果
            result = self.analyzer.analyze(job)
            
            if result:
                # 更新分析结果
                analysis.salary_min = result.get('salary_min')
                analysis.salary_max = result.get('salary_max')
                analysis.salary_fixed = result.get('salary_fixed')
                analysis.salary_currency = result.get('salary_currency')
                analysis.skill_tags = ', '.join(result.get('skill_tags', []))
                analysis.experience_level = result.get('experience_level')
                analysis.summary = result.get('summary')
                analysis.status = 'completed'
            else:
                analysis.status = 'failed'
            session.commit()
            logger.info(f"Successfully analyzed job {job.id}")
            
        except Exception as e:
            logger.error(f"Error analyzing job {job.id}: {str(e)}")
            if analysis:
                analysis.status = 'failed'
                session.commit()
    
    def run(self, interval: int = 60):
        """运行服务"""
        logger.info("Job Analysis Service started")
        
        while True:
            try:
                with Session(self.engine) as session:
                    # 获取一批待处理的工作
                    jobs = self.get_pending_jobs(session)
                    
                    if not jobs:
                        logger.info("No pending jobs found, waiting...")
                        time.sleep(interval)
                        continue
                    
                    # 处理每个工作
                    for job in jobs:
                        self.analyze_job(session, job)
                        
            except Exception as e:
                logger.error(f"Error in main loop: {str(e)}")
                time.sleep(interval)
