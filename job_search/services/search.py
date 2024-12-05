from sqlalchemy import or_, and_
from sqlalchemy.orm import Session
from data_storage.models import Job, Company, JobAnalysis
from datetime import datetime
from typing import List, Optional
from ..schemas.job import JobBrief, JobDetail, CompanyBrief, JobSearchResult, SalaryRange

class JobSearchService:
    def __init__(self, db: Session):
        self.db = db

    def search_jobs(
        self,
        query: Optional[str] = None,
        company_ids: Optional[List[str]] = None,
        employment_types: Optional[List[str]] = None,
        posted_after: Optional[datetime] = None,
        is_remote: Optional[bool] = None,
        page: int = 1,
        per_page: int = 20
    ):
        query_filters = []
        
        # Base query - join with JobAnalysis
        base_query = self.db.query(Job).join(Company).join(JobAnalysis)
        
        # Add completed status filter for JobAnalysis
        query_filters.append(JobAnalysis.status == 'completed')
        
        # Add other filters
        if query:
            query_filters.append(
                or_(
                    Job.title.ilike(f"%{query}%"),
                    Job.full_description.ilike(f"%{query}%")
                )
            )
        
        if company_ids:
            query_filters.append(Job.company_id.in_(company_ids))
            
        if employment_types:
            query_filters.append(
                Job.employment_type.in_(employment_types)
            )
            
        if posted_after:
            query_filters.append(
                Job.posted_date >= posted_after
            )
            
        if is_remote is not None:
            query_filters.append(Job.is_remote == is_remote)
            
        # Add not expired filter
        query_filters.append(Job.expired == False)
        
        # Apply filters
        base_query = base_query.filter(and_(*query_filters))
        
        # Order by posted date
        base_query = base_query.order_by(Job.posted_date.desc())
        
        # Get total count
        total = base_query.count()
        
        # Add pagination
        results = base_query.offset((page - 1) * per_page).limit(per_page).all()
        
        # Convert SQLAlchemy models to dicts
        job_briefs = [self._convert_to_job_brief(job) for job in results]
        
        return JobSearchResult(
            total=total,
            page=page,
            per_page=per_page,
            results=job_briefs
        )

    def get_job_detail(self, job_id: str) -> JobDetail:
        job = self.db.query(Job).filter(Job.id == job_id).first()
        return self._convert_to_job_detail(job)

    def _convert_to_job_brief(self, job: Job) -> JobBrief:
        """Convert SQLAlchemy Job model to JobBrief model"""
        salary_range, experience_level, skill_tags, summary = self._get_job_analysis_data(job)
        
        return JobBrief(
            id=job.id,
            title=job.title,
            company=CompanyBrief(
                id=job.company.id,
                name=job.company.name,
                icon_url=job.company.icon_url
            ),
            location=job.location,
            employment_type=job.employment_type,
            posted_date=job.posted_date,
            is_remote=job.is_remote,
            url=job.url,
            salary_range=salary_range,
            experience_level=experience_level,
            skill_tags=skill_tags,
            summary=summary
        )
    
    def _convert_to_job_detail(self, job: Job) -> JobDetail:
        """Convert SQLAlchemy Job model to JobDetail model"""
        salary_range, experience_level, skill_tags, summary = self._get_job_analysis_data(job)
        
        return JobDetail(
            id=job.id,
            title=job.title,
            company=CompanyBrief(
                id=job.company.id,
                name=job.company.name,
                icon_url=job.company.icon_url
            ),
            location=job.location,
            employment_type=job.employment_type,
            posted_date=job.posted_date,
            is_remote=job.is_remote,
            url=job.url,
            salary_range=salary_range,
            experience_level=experience_level,
            skill_tags=skill_tags,
            summary=summary,
            full_description=job.full_description  # 这是JobDetail特有的字段
        )

    def _get_job_analysis_data(self, job: Job) -> tuple:
        """Extract common analysis data from job"""
        salary_range = None
        experience_level = None
        skill_tags = None
        summary = None
        
        if job.analysis:
            salary_range = SalaryRange(
                min=job.analysis.salary_min,
                max=job.analysis.salary_max,
                fixed=job.analysis.salary_fixed,
                currency=job.analysis.salary_currency
            )
            experience_level = job.analysis.experience_level if job.analysis.experience_level else None
            skill_tags = job.analysis.skill_tags.split(',') if job.analysis.skill_tags else []
            summary = job.analysis.summary
            
        return salary_range, experience_level, skill_tags, summary