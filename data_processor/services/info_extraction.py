import signal
import sys
import threading
import time
import logging
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy.orm import Session, joinedload
from typing import List, Set
from data_storage.config import create_db_engine
from data_storage.models import Job, JobAnalysis
from data_processor.processors import InfoExtractingProcessor

logger = logging.getLogger(__name__)

class InfoExtractionService:
    def __init__(self, max_workers: int = 5):
        self.engine = create_db_engine()
        self.current_analyses: Set[int] = set()
        self.lock = threading.Lock()
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=self.max_workers)
        self.processor = InfoExtractingProcessor(llm_provider='moonshot')
        
        # Register signal handlers
        signal.signal(signal.SIGINT, self._handle_shutdown)
        signal.signal(signal.SIGTERM, self._handle_shutdown)

    def run(self, interval: int = 60):
        """Run the info extraction service"""
        logger.info("Info Extraction Service started")
        
        while True:
            try:
                with Session(self.engine) as session:
                    jobs = self._get_pending_jobs(session)
                    
                if not jobs:
                    logger.info("No pending jobs found, waiting...")
                    time.sleep(interval)
                    continue
                
                futures = []
                for job in jobs:
                    thread_session = Session(self.engine)
                    future = self.executor.submit(self._process_job, thread_session, job)
                    futures.append((future, thread_session))
                
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

    def _get_pending_jobs(self, session: Session, batch_size: int = None) -> List[Job]:
        """Get jobs pending for analysis"""
        if batch_size is None:
            batch_size = self.max_workers * 2
            
        return (
            session.query(Job)
            .options(joinedload(Job.company))
            .join(JobAnalysis)
            .filter(JobAnalysis.status.in_(['pending', 'failed']))
            .limit(batch_size)
            .all()
        )

    def _process_job(self, session: Session, job: Job):
        """Process a single job"""
        analysis = None
        try:
            analysis = session.query(JobAnalysis).filter_by(job_id=job.id).first()
            if not analysis:
                analysis = JobAnalysis(job_id=job.id)
                session.add(analysis)
            
            analysis.status = 'processing'
            session.commit()
            
            with self.lock:
                self.current_analyses.add(analysis.id)
            
            result = self.processor.process(job)
            
            if result:
                self._save_analysis(analysis, result, session)
                analysis.status = 'processed'
                logger.info(f"Successfully extracted info from job {job.id}")
            else:
                analysis.status = 'failed'
            session.commit()
            
        except Exception as e:
            logger.error(f"Error extracting info from job {job.id}: {str(e)}")
            if analysis:
                analysis.status = 'failed'
                session.commit()
        finally:
            with self.lock:
                self.current_analyses.discard(analysis.id if analysis else None)

    def _save_analysis(self, analysis: JobAnalysis, result: dict, session: Session):
        """Save analysis results to database"""
        # Save salary information
        analysis.salary_min = result.get('salary_min')
        analysis.salary_max = result.get('salary_max')
        analysis.salary_fixed = result.get('salary_fixed')
        analysis.salary_currency = result.get('salary_currency')
        analysis.salary_period = result.get('salary_period')
        analysis.is_salary_estimated = result.get('is_salary_estimated')
        
        # Save other extracted information
        analysis.skill_tags = result.get('skill_tags')
        analysis.experience_level = result.get('experience_level')
        analysis.summary = result.get('summary')
        
        session.commit()

    def _handle_shutdown(self, signum, frame):
        """Handle termination signals"""
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
