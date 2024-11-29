from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ....schemas.job import JobSearchParams, JobBrief, JobDetail
from ....services.search import JobSearchService
from ....api.deps import get_db
from data_storage.models import Job

router = APIRouter()

@router.get("/search", response_model=dict)
async def search_jobs(
    db: Session = Depends(get_db),
    params: JobSearchParams = Depends()
):
    search_service = JobSearchService(db)
    return search_service.search_jobs(
        query=params.q,
        company_ids=params.company_ids,
        employment_types=params.employment_types,
        posted_after=params.posted_after,
        is_remote=params.is_remote,
        page=params.page,
        per_page=params.per_page
    )

@router.get("/detail", response_model=JobDetail)
async def get_job_detail(
    job_id: str = Query(...),
    db: Session = Depends(get_db)
):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job 