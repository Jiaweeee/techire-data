# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class JobItem:
    company_id: str
    title: str
    url: str
    full_description: str # Should be markdown
    job_id: Optional[str] = None # Company specific
    posted_date: Optional[str] = None
    employment_type: Optional[str] = None
    locations: List[str] = field(default_factory=list)
    skill_tags: List[str] = field(default_factory=list) # Extracted by AI
    salary_range: Optional[str] = None # Extracted by AI
    expired: bool = False
