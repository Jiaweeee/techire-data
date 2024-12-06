from fastapi import APIRouter, HTTPException
from ....schemas import JobSearchParams, JobSearchResponse, JobDetail
from ....services.job_search import JobSearchService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/search", response_model=JobSearchResponse)
async def search_jobs(params: JobSearchParams):
    search_service = JobSearchService()
    return search_service.search_jobs(params)

@router.get("/detail", response_model=JobDetail)
async def job_detail(job_id: str):
    job = None
    try:
        search_service = JobSearchService()
        job = search_service.get_job_detail(job_id)
    except Exception as e:
        logger.error(f"Error getting job detail: {e}")
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
