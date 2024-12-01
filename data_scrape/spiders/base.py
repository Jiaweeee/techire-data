import scrapy
from data_scrape.items import JobItem
from data_storage.crud import CompanyCRUD
from abc import ABC, abstractmethod
from typing import List
from bs4 import BeautifulSoup

class BasePagingJobSpider(scrapy.Spider, ABC):
    """
    Base class for spiders that need to scrape job listings with pagination.
    """
    def __init__(self, *args, **kwargs):
        super(BasePagingJobSpider, self).__init__(*args, **kwargs)
        self.company = CompanyCRUD().get_by_code(self.name)

    def start_requests(self):
        start_url = self.get_start_url()
        yield scrapy.Request(url=start_url, callback=self.parse_first_page)

    def parse_first_page(self, response):
        total_jobs = self.get_total_jobs(response)
        page_size = self.get_page_size()
        total_pages = total_jobs // page_size + (1 if total_jobs % page_size > 0 else 0)
        
        for page in range(1, total_pages + 1):
            url = self.get_page_url(page, page_size)
            yield scrapy.Request(
                url=url, 
                callback=self.parse_list,
                dont_filter=self.should_disable_filter()
            )

    def parse_list(self, response):
        job_urls = self.extract_job_urls(response)
        for url in job_urls:
            yield scrapy.Request(url=url, callback=self.parse_detail)

    def parse_detail(self, response):
        job_data = self.extract_job_data(response)
        yield JobItem(**job_data)
    
    def sanitize_html(self, html: str | None) -> str:
        if not html:
            return "<p>No information provided</p>"
        
        # 保留原始HTML结构，但清理不必要的属性和样式
        soup = BeautifulSoup(html, 'html.parser')
        
        # 移除所有样式属性和类名（因为这些可能与原网站样式相关）
        for tag in soup.find_all(True):
            tag.attrs = {key: value for key, value in tag.attrs.items() 
                        if key not in ['class', 'style']}
        
        return str(soup)

    # Abstract methods that need to be implemented by subclasses
    @abstractmethod
    def get_start_url(self) -> str:
        """Return the initial URL to start scraping"""
        pass

    @abstractmethod
    def get_total_jobs(self, response) -> int:
        """Extract total number of jobs from first page response"""
        pass

    @abstractmethod
    def get_page_size(self) -> int:
        """Return the number of jobs per page"""
        pass

    @abstractmethod
    def get_page_url(self, page: int, page_size: int) -> str:
        """Generate URL for specific page"""
        pass

    @abstractmethod
    def extract_job_urls(self, response) -> List[str]:
        """Extract job URLs from list page"""
        pass

    @abstractmethod
    def extract_job_data(self, response) -> dict:
        """Extract job details from detail page"""
        pass

    def should_disable_filter(self) -> bool:
        """Override if need to disable duplicate filter"""
        return False