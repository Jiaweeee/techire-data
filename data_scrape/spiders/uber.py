import scrapy
import json
import markdown
from data_scrape.items import JobItem
from data_storage.crud import CompanyCRUD
from bs4 import BeautifulSoup

class UberSpider(scrapy.Spider):
    name = "uber"
    
    def __init__(self, *args, **kwargs):
        super(UberSpider, self).__init__(*args, **kwargs)
        self.company = CompanyCRUD().get_by_code(self.name)
        self.active_job_urls = set()
        self.total_jobs = 0
        self.processed_jobs = 0
        self.crawl_successful = False
        self.page_size = 10
    
    def start_requests(self):
        """第一个请求"""
        yield scrapy.Request(
            url="https://www.uber.com/api/loadSearchJobsResults?localeCode=en",
            method='POST',
            headers={
                'User-Agent': 'PostmanRuntime/7.43.0',
                'x-csrf-token': 'x',
                'Content-Type': 'application/json',
                'Cookie': '__cf_bm=hEUe7_kasqSC.KWWcWh1m.FFFZrA1vy8Wy_n0XEg3S8-1733988355-1.0.1.1-mbkdKaVEBz8gXAvgd.ojzJK9_lE_gkyeeG44w_J.4AoyhLE73StJhGL8gQzLYCXQJwOGLxj5732rM4vTQM_xnA; _ua={"session_id":"74e00138-0262-4bb8-906c-01f869a4d5fb","session_time_ms":1733971257237}; jwt-session=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InNsYXRlLWV4cGlyZXMtYXQiOjE3MzM5OTAwNTU0NDR9LCJpYXQiOjE3MzM5NzA5OTUsImV4cCI6MTczNDA1NzM5NX0.SOrq4tSnrQxYgkpdCm3mW3oxsE8Rpsx4AZfiFYB0oHM; user_city_ids=965'
            },
            body=json.dumps({
                "limit": self.page_size,
                "page": 0,
                "params": {
                    "department": [],
                    "lineOfBusinessName": [],
                    "location": [],
                    "programAndPlatform": [],
                    "team": []
                }
            }),
            callback=self.parse_first_page,
            dont_filter=True
        )
    
    def parse_first_page(self, response):
        """处理第一页并发起后续请求"""
        data = response.json()
        self.total_jobs = data['data']['totalResults']['low']
        total_pages = (self.total_jobs + self.page_size - 1) // self.page_size
        
        # 处理第一页数据
        for job in data['data']['results']:
            job_item = self._parse_job_data(job)
            self.active_job_urls.add(job_item.url)
            self.processed_jobs += 1
            yield job_item
        
        # 处理剩余页面
        for page in range(1, total_pages):
            yield scrapy.Request(
                url="https://www.uber.com/api/loadSearchJobsResults?localeCode=en",
                method='POST',
                headers={
                    'x-csrf-token': 'x',
                    'Content-Type': 'application/json',
                    'Cookie': '__cf_bm=hEUe7_kasqSC.KWWcWh1m.FFFZrA1vy8Wy_n0XEg3S8-1733988355-1.0.1.1-mbkdKaVEBz8gXAvgd.ojzJK9_lE_gkyeeG44w_J.4AoyhLE73StJhGL8gQzLYCXQJwOGLxj5732rM4vTQM_xnA; _ua={"session_id":"74e00138-0262-4bb8-906c-01f869a4d5fb","session_time_ms":1733971257237}; jwt-session=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InNsYXRlLWV4cGlyZXMtYXQiOjE3MzM5OTAwNTU0NDR9LCJpYXQiOjE3MzM5NzA5OTUsImV4cCI6MTczNDA1NzM5NX0.SOrq4tSnrQxYgkpdCm3mW3oxsE8Rpsx4AZfiFYB0oHM; user_city_ids=965'
                },
                body=json.dumps({
                    "limit": self.page_size,
                    "page": page,
                    "params": {
                        "department": [],
                        "lineOfBusinessName": [],
                        "location": [],
                        "programAndPlatform": [],
                        "team": []
                    }
                }),
                callback=self.parse_page,
                dont_filter=True,
                meta={'page': page}
            )
    
    def parse_page(self, response):
        """处理后续页面"""
        try:
            data = response.json()
            if not data or 'data' not in data or 'results' not in data['data']:
                self.logger.error(f"Invalid API response format: {data}")
                return
            total_jobs = data['data']['totalResults']['low']
            if total_jobs != self.total_jobs:
                self.total_jobs = total_jobs
            page = response.meta.get('page', 0)
            jobs = data['data']['results']
            if not jobs:
                self.logger.info(f"Page {page}: No jobs found")
                return
            
            self.logger.info(f"Page {page}: Found {len(jobs)} jobs")
            processed_count = 0
            
            for job in jobs:
                try:
                    job_item = self._parse_job_data(job)
                    self.active_job_urls.add(job_item.url)
                    self.processed_jobs += 1
                    processed_count += 1
                    yield job_item
                except Exception as e:
                    self.logger.error(f"Error processing job: {str(e)}")
                    self.logger.error(f"Job data: {job}")
            
            self.logger.info(f"Page {page}: Successfully processed {processed_count}/{len(jobs)} jobs")
            self.logger.info(f"Total processed: {self.processed_jobs}/{self.total_jobs} jobs")
            
            if self.processed_jobs >= self.total_jobs:
                self.crawl_successful = True
                
        except Exception as e:
            self.logger.error(f"Error processing page: {str(e)}")
            self.logger.error(f"Response content: {response.text}")
    
    def _parse_job_data(self, job: dict) -> JobItem:
        """解析单个工作数据"""
        locations = []
        if job.get('allLocations'):
            for loc in job['allLocations']:
                location_parts = []
                if loc.get('city'):
                    location_parts.append(loc['city'])
                if loc.get('region'):
                    location_parts.append(loc['region'])
                if loc.get('countryName'):
                    location_parts.append(loc['countryName'])
                if location_parts:
                    locations.append(', '.join(location_parts))
        
        return JobItem(
            company_id=self.company.id,
            title=job['title'],
            url=f"https://www.uber.com/global/en/careers/list/{job['id']}",
            full_description=self._sanitize_html(job['description']),
            raw_posted_date=job.get('creationDate'),
            raw_employment_type=job.get('timeType', ''),
            locations=locations,
            expired=job.get('statusName') != 'Approved'
        )
    
    def _sanitize_html(self, markdown_text: str | None) -> str:
        """将 Markdown 转换为 HTML"""
        if not markdown_text:
            return "<p>No information provided</p>"
        
        # 将 Markdown 转换为 HTML
        html = markdown.markdown(
            markdown_text,
            extensions=['extra']  # 支持表格等扩展语法
        )
        
        # 如果需要的话，还可以用 BeautifulSoup 进一步清理 HTML
        soup = BeautifulSoup(html, 'html.parser')
        for tag in soup.find_all(True):
            tag.attrs = {key: value for key, value in tag.attrs.items() 
                        if key not in ['class', 'style']}
        
        return str(soup)
    
    def closed(self, reason):
        """爬虫关闭时的处理"""
        if self.crawl_successful:
            self.logger.info(
                f"Spider {self.name} completed successfully. "
                f"Found {len(self.active_job_urls)} active jobs."
            )
        else:
            self.logger.warning(
                f"Spider {self.name} did not complete successfully. "
                f"Reason: {reason}. "
                f"Processed {self.processed_jobs}/{self.total_jobs} jobs."
            )