from pydantic import BaseModel
from typing import Optional

class CompanyBrief(BaseModel):
    id: str
    name: str
    icon_url: Optional[str] = None

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