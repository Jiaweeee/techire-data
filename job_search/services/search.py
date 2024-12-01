from sqlalchemy import or_, and_
from sqlalchemy.orm import Session
from data_storage.models import Job, Company
from datetime import datetime
from typing import List, Optional

class JobSearchService:
    def __init__(self, db: Session):
        self.db = db

    def _convert_to_job_brief(self, job: Job) -> dict:
        """Convert SQLAlchemy Job model to dict for serialization"""
        return {
            "id": job.id,
            "title": job.title,
            "company": {
                "id": job.company.id,
                "name": job.company.name,
                "icon_url": job.company.icon_url
            },
            "location": job.location,
            "employment_type": job.employment_type,
            "posted_date": job.normalized_posted_date,
            "salary_range": job.salary_range,
            "is_remote": job.is_remote,
            "url": job.url
        }

    def search_jobs(
        self,
        query: Optional[str] = None,
        company_ids: Optional[List[str]] = None,
        employment_types: Optional[List[str]] = None,  # 修改参数名
        posted_after: Optional[datetime] = None,
        is_remote: Optional[bool] = None,
        page: int = 1,
        per_page: int = 20
    ):
        query_filters = []
        
        # Base query
        base_query = self.db.query(Job).join(Company)
        
        # Add filters
        if query:
            query_filters.append(
                or_(
                    Job.title.ilike(f"%{query}%"),
                    Job.full_description.ilike(f"%{query}%")
                )
            )
        
        if company_ids:
            query_filters.append(Job.company_id.in_(company_ids))
            
        if employment_types:  # 修改这里
            query_filters.append(
                Job.employment_type.in_(employment_types)
            )
            
        if posted_after:
            query_filters.append(
                Job.normalized_posted_date >= posted_after
            )
            
        if is_remote is not None:
            query_filters.append(Job.is_remote == is_remote)
            
        # Add not expired filter
        query_filters.append(Job.expired == False)
        
        # Apply filters
        if query_filters:
            base_query = base_query.filter(and_(*query_filters))
            
        # Order by posted date
        base_query = base_query.order_by(Job.normalized_posted_date.desc())
        
        # Get total count
        total = base_query.count()
        
        # Add pagination
        results = base_query.offset((page - 1) * per_page).limit(per_page).all()
        
        # Convert SQLAlchemy models to dicts
        job_briefs = [self._convert_to_job_brief(job) for job in results]
        
        return {
            "total": total,
            "page": page,
            "per_page": per_page,
            "results": job_briefs
        }