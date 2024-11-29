from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

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

class JobBrief(BaseModel):
    id: str
    title: str
    company: CompanyBrief
    location: str
    employment_type: Optional[str]
    normalized_employment_type: Optional[str]
    posted_date: Optional[datetime]
    salary_range: Optional[str]
    is_remote: Optional[bool]
    
    class Config:
        from_attributes = True

class JobDetail(JobBrief):
    full_description: str
    skill_tags: Optional[str]
    
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