# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass, field
from typing import Optional, List, Union
from datetime import datetime

@dataclass
class JobItem:
    company_id: str
    title: str
    url: str
    full_description: str
    raw_posted_date: Optional[Union[str, int, float]] = None
    raw_employment_type: Optional[str] = None
    locations: List[str] = field(default_factory=list)
    expired: bool = False
