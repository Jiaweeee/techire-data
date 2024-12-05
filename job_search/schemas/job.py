from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from data_storage.models import EmploymentType
class CompanyBrief(BaseModel):
    id: str
    name: str
    icon_url: str
    
    class Config:
        from_attributes = True

class CompanyDetail(CompanyBrief):
    code: str
    official_site_url: str
    careers_page_url: str
    introduction: str
    industry: Optional[str]
    headquarters: Optional[str]
    
    class Config:
        from_attributes = True

class SalaryRange(BaseModel):
    min: Optional[int] = None
    max: Optional[int] = None
    fixed: Optional[int] = None
    currency: Optional[str] = None

class JobBrief(BaseModel):
    id: str
    title: str
    company: CompanyBrief
    location: str
    employment_type: Optional[EmploymentType]
    posted_date: Optional[datetime]
    is_remote: Optional[bool]
    url: str
    salary_range: Optional[SalaryRange] = None
    experience_level: Optional[int] = None
    skill_tags: Optional[List[str]] = None
    summary: Optional[str] = None
    
    class Config:
        from_attributes = True

class JobDetail(JobBrief):
    full_description: str
    
    class Config:
        from_attributes = True

class JobSearchParams(BaseModel):
    q: Optional[str] = None
    company_ids: Optional[List[str]] = None
    employment_types: Optional[List[str]] = None
    posted_after: Optional[datetime] = None
    is_remote: Optional[bool] = None
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=20, ge=1, le=100) 

class JobSearchResult(BaseModel):
    total: int
    page: int
    per_page: int
    results: List[JobBrief]