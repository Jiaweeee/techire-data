import signal
import sys
import logging
from sqlalchemy.orm import Session
from data_storage.config import create_db_engine
from data_storage.models import Job, JobAnalysis
from .analyzer import JobAnalyzer
import time
from concurrent.futures import ThreadPoolExecutor
import threading
from .processors import InfoExtractingProcessor, DataIndexingProcessor


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JobProcessingService:
    def __init__(self):
        self.engine = create_db_engine()
        self.analyzer = JobAnalyzer()
        self.current_analyses = set()  # 使用 set 存储当前正在处理的分析 ID
        self.lock = threading.Lock()  # 用于同步访问 current_analyses
        
        # 设置线程池
        self.max_workers = 5  # 可以根据需求调整并发数
        self.executor = ThreadPoolExecutor(max_workers=self.max_workers)
        self.processors = {
            'extracting': InfoExtractingProcessor(),
            'indexing': DataIndexingProcessor()
        }
        
        signal.signal(signal.SIGINT, self._handle_shutdown)
        signal.signal(signal.SIGTERM, self._handle_shutdown)
    
    def run(self, interval: int = 60):
        """运行服务"""
        logger.info("Job Analysis Service started")

        for processor in self.processors.values():
            processor.setup()
        
        while True:
            try:
                jobs = None
                with Session(self.engine) as session:
                    jobs = self._get_pending_jobs(session, batch_size=self.max_workers * 2)
                    
                if not jobs:
                    logger.info("No pending jobs found, waiting...")
                    time.sleep(interval)
                    continue
                
                # 创建新的 Session 对象给每个线程
                futures = []
                for job in jobs:
                    thread_session = Session(self.engine)
                    future = self.executor.submit(self._process_job, thread_session, job)
                    futures.append((future, thread_session))
                
                # 等待所有任务完成并关闭 sessions
                for future, thread_session in futures:
                    try:
                        future.result()
                    except Exception as e:
                        logger.error(f"Thread execution error: {str(e)}")
                    finally:
                        thread_session.close()
                            
            except Exception as e:
                logger.error(f"Error in main loop: {str(e)}")
                time.sleep(interval)
    
    def _get_pending_jobs(self, session: Session, batch_size: int = 10):
        return (
            session.query(Job)
            .join(JobAnalysis)
            .filter(JobAnalysis.status.in_(['pending', 'failed']))
            .limit(batch_size)
            .all()
        )
    
    def _process_job(self, session: Session, job: Job):
        """分析单个工作"""
        analysis = None
        try:
            analysis = session.query(JobAnalysis).filter_by(job_id=job.id).first()
            if not analysis:
                analysis = JobAnalysis(job_id=job.id)
                session.add(analysis)
            
            analysis.status = 'processing'
            session.commit()
            
            # 将分析 ID 添加到当前处理集合
            with self.lock:
                self.current_analyses.add(analysis.id)
            
            result = self.processors['extracting'].process(job)
            
            if result:
                self._save_analysis(analysis, result, session)
                
                job = session.merge(job)
                self.processors['indexing'].process(job)
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
        finally:
            # 从当前处理集合中移除分析 ID
            with self.lock:
                self.current_analyses.discard(analysis.id if analysis else None)
    
    def _save_analysis(self, analysis, result, session: Session):
        analysis.salary_min = result.get('salary_min')
        analysis.salary_max = result.get('salary_max')
        analysis.salary_fixed = result.get('salary_fixed')
        analysis.salary_currency = result.get('salary_currency')
        analysis.skill_tags = result.get('skill_tags')
        analysis.experience_level = result.get('experience_level')
        analysis.summary = result.get('summary')
        session.commit()

    def _handle_shutdown(self, signum, frame):
        """处理终止信号"""
        logger.info("Received shutdown signal, cleaning up...")
        
        self.executor.shutdown(wait=False)
        
        with Session(self.engine) as session:
            with self.lock:
                for analysis_id in self.current_analyses:
                    try:
                        analysis = session.query(JobAnalysis).get(analysis_id)
                        if analysis and analysis.status == 'processing':
                            analysis.status = 'failed'
                    except Exception as e:
                        logger.error(f"Error during cleanup: {str(e)}")
                session.commit()
        
        logger.info("Cleanup completed, shutting down...")
        sys.exit(0)
