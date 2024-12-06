from pydantic import BaseModel
from typing import List, Optional
from .company import CompanyBrief

class JobSearchParams(BaseModel):
    q: Optional[str] = None
    location: Optional[str] = None
    employment_type: Optional[str] = None
    is_remote: Optional[bool] = None
    company_ids: Optional[List[str]] = None
    page: int = 1
    per_page: int = 10

class SalaryRange(BaseModel):
    min: Optional[float] = None
    max: Optional[float] = None
    fixed: Optional[float] = None
    currency: Optional[str] = None

class JobBrief(BaseModel):
    id: str
    title: str
    company: CompanyBrief
    location: Optional[str] = None
    employment_type: Optional[int] = None
    posted_date: Optional[str] = None
    is_remote: Optional[bool] = False
    url: str
    skill_tags: Optional[List[str]] = []
    summary: Optional[str] = None
    salary_range: Optional[SalaryRange] = None
    experience_level: Optional[int] = None
    score: Optional[float] = 0.0

class JobDetail(JobBrief):
    full_description: str

class JobSearchResponse(BaseModel):
    total: int
    results: List[JobBrief] = []
    page: int
    per_page: int 