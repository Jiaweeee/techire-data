import time
import signal
from sqlalchemy.orm import Session, joinedload
from typing import List
from data_storage.config import create_db_engine
from data_storage.models import Job, JobAnalysis
from data_processor.processors import DataIndexingProcessor
import logging

logger = logging.getLogger(__name__)

class JobIndexService:
    def __init__(self, batch_size: int = 1000):
        self.engine = create_db_engine()
        self.batch_size = batch_size
        self.processor = DataIndexingProcessor()
        self.should_continue = True
        
        # 设置信号处理
        signal.signal(signal.SIGTERM, self._handle_shutdown)
        signal.signal(signal.SIGINT, self._handle_shutdown)

    def _handle_shutdown(self, signum, frame):
        """处理关闭信号"""
        logger.info("Received shutdown signal, stopping gracefully...")
        self.should_continue = False

    def run(self, interval: int = 300):
        logger.info("Job Index Service started")
        
        while self.should_continue:
            try:
                processed_count = 0
                with Session(self.engine) as session:
                    while self.should_continue:
                        jobs = self._get_unindexed_jobs(session)
                        if not jobs:
                            break
                            
                        for job in jobs:
                            if not self.should_continue:
                                break
                            try:
                                self.processor.process(job)
                                db_job = session.merge(job)
                                db_job.analysis.status = 'indexed'
                                processed_count += 1
                            except Exception as e:
                                print(f"Error indexing job {job.id}: {str(e)}")
                        
                        if processed_count > 0:
                            session.commit()
                            logger.info(f"Indexed {processed_count} jobs")
                
                if processed_count == 0 and self.should_continue:
                    logger.info("No jobs to index, waiting...")
                    for _ in range(interval):
                        if not self.should_continue:
                            break
                        time.sleep(1)
                    
            except Exception as e:
                logger.error(f"Error in indexing loop: {str(e)}")
                if self.should_continue:
                    for _ in range(interval):
                        if not self.should_continue:
                            break
                        time.sleep(1)

        logger.info("Job Index Service stopped")

    def _get_unindexed_jobs(self, session: Session) -> List[Job]:
        """Get jobs that need to be indexed"""
        return (
            session.query(Job)
            .options(
                joinedload(Job.company),
                joinedload(Job.analysis)
            )
            .join(JobAnalysis)
            .filter(JobAnalysis.status == 'processed')
            .limit(self.batch_size)
            .all()
        )
