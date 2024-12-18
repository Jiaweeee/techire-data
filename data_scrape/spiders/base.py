import scrapy
from data_scrape.items import JobItem
from data_storage.crud import CompanyCRUD, JobCRUD
from abc import ABC, abstractmethod
from typing import List
from bs4 import BeautifulSoup
import markdown

class BasePagingJobSpider(scrapy.Spider, ABC):
    """
    Base class for spiders that need to scrape job listings with pagination.
    """
    def __init__(self, *args, **kwargs):
        super(BasePagingJobSpider, self).__init__(*args, **kwargs)
        self.company = CompanyCRUD().get_by_code(self.name)
        self.active_job_urls = set()
        self.crawl_successful = False
        self.total_jobs = 0
        self.processed_jobs = 0

    def start_requests(self):
        start_url = self.get_start_url()
        yield scrapy.Request(url=start_url, callback=self.parse_first_page)

    def parse_first_page(self, response):
        self.total_jobs = self.get_total_jobs(response)
        page_size = self.get_page_size()
        total_pages = self.total_jobs // page_size + (1 if self.total_jobs % page_size > 0 else 0)
        
        for page in range(1, total_pages + 1):
            url = self.get_page_url(page, page_size)
            yield scrapy.Request(
                url=url, 
                callback=self.parse_list,
                dont_filter=self.should_disable_filter()
            )

    def parse_list(self, response):
        job_urls = self.extract_job_urls(response)
        self.active_job_urls.update(job_urls)
        self.processed_jobs += len(job_urls)
        
        # 检查是否已处理完所有工作
        if self.processed_jobs >= self.total_jobs:
            self.crawl_successful = True
            
        for url in job_urls:
            yield scrapy.Request(url=url, callback=self.parse_detail)

    def parse_detail(self, response):
        job_item = self.extract_job_data(response)
        yield job_item
    
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

    def sanitize_description(self, content: str | None, content_type: str = 'html') -> str:
        """统一处理职位描述的格式
        
        Args:
            content: 原始内容
            content_type: 内容类型 ('html', 'markdown', 或 'plaintext')
        """
        if not content:
            return "<p>No information provided</p>"
        
        # 如果是纯文本，先将换行符转换为HTML段落
        if content_type == 'plaintext':
            paragraphs = content.split('\n')
            content = ''.join([f"<p>{p}</p>" for p in paragraphs if p.strip()])
            content_type = 'html'  # 转换后按HTML处理
            
        # 如果是 markdown 格式，先转换为 HTML
        if content_type == 'markdown':
            content = markdown.markdown(content, extensions=['extra'])
            
        # 使用 BeautifulSoup 统一处理 HTML
        soup = BeautifulSoup(content, 'html.parser')
        
        # 保留允许的标签和属性
        allowed_tags = {'p', 'br', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 
                       'ul', 'ol', 'li', 'strong', 'em', 'a', 'section'}
        allowed_attrs = {'href': ['a']}  # 只允许 a 标签保留 href 属性
        
        for tag in soup.find_all(True):
            if tag.name not in allowed_tags:
                tag.unwrap()  # 移除标签但保留内容
            else:
                # 清理属性
                allowed = allowed_attrs.get(tag.name, [])
                tag.attrs = {key: value for key, value in tag.attrs.items() 
                           if key in allowed}
        
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
    def extract_job_data(self, response) -> JobItem:
        """Extract job details from detail page"""
        pass

    def should_disable_filter(self) -> bool:
        """Override if need to disable duplicate filter"""
        return False

    def closed(self, reason):
        """Spider关闭时被调用"""
        # 只在爬取成功完成时更新过期状态
        if self.crawl_successful:
            job_crud = JobCRUD()
            updated_count = job_crud.mark_jobs_expired(
                self.company.id, 
                self.active_job_urls
            )
            self.logger.info(
                f"Spider {self.name} completed successfully. "
                f"Marked {updated_count} jobs as expired. "
                f"Found {len(self.active_job_urls)} active jobs."
            )
        else:
            self.logger.warning(
                f"Spider {self.name} did not complete successfully. "
                f"Reason: {reason}. "
                f"Processed {self.processed_jobs}/{self.total_jobs} jobs. "
                f"No jobs will be marked as expired."
            )