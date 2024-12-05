from pydantic import BaseModel
from typing import List, Optional

class Company(BaseModel):
    id: str
    name: str

class SearchParams(BaseModel):
    q: Optional[str] = None
    location: Optional[str] = None
    employment_type: Optional[str] = None
    is_remote: Optional[bool] = None
    company_ids: Optional[List[str]] = None
    page: int = 1
    per_page: int = 10

class SearchResult(BaseModel):
    id: str
    title: str
    company: Company
    location: Optional[str] = None
    employment_type: Optional[str] = None
    posted_date: Optional[str] = None
    is_remote: Optional[bool] = False
    skill_tags: Optional[List[str]] = []
    score: Optional[float] = 0.0

class SearchResponse(BaseModel):
    total: int
    results: List[SearchResult]
    page: int
    per_page: int 