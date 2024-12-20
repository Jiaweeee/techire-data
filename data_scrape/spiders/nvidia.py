import scrapy
import json
from data_scrape.items import JobItem
from data_scrape.spiders.base import BasePagingJobSpider
from typing import List

class NvidiaSpider(BasePagingJobSpider):
    name = "nvidia"
    
    def get_start_url(self) -> str:
        return "https://nvidia.wd5.myworkdayjobs.com/wday/cxs/nvidia/NVIDIAExternalCareerSite/jobs"

    def get_total_jobs(self, response) -> int:
        data = response.json()
        # 从 facets 中获取所有工作数量的总和
        job_categories = data['facets'][0]['values']
        return sum(category['count'] for category in job_categories)

    def get_page_size(self) -> int:
        return 20

    def get_page_url(self, page: int, page_size: int) -> str:
        # Workday API 使用 POST 请求，这个 URL 不会被直接使用
        return self.get_start_url()

    def should_disable_filter(self) -> bool:
        return True

    def start_requests(self):
        """覆盖父类方法使用 POST 请求"""
        yield scrapy.Request(
            url=self.get_start_url(),
            method='POST',
            headers={'Content-Type': 'application/json'},
            body=json.dumps({
                "appliedFacets": {},
                "limit": self.get_page_size(),
                "offset": 0,
                "searchText": ""
            }),
            callback=self.parse_first_page,
            dont_filter=True
        )

    def parse_first_page(self, response):
        """处理第一页并发起后续请求"""
        total_jobs = self.get_total_jobs(response)
        self.total_jobs = total_jobs
        total_pages = (total_jobs + self.get_page_size() - 1) // self.get_page_size()
        
        # 处理第一页数据
        yield from self.parse_list(response)
        
        # 处理剩余页面
        for page in range(1, total_pages):
            offset = page * self.get_page_size()
            yield scrapy.Request(
                url=self.get_start_url(),
                method='POST',
                headers={'Content-Type': 'application/json'},
                body=json.dumps({
                    "appliedFacets": {},
                    "limit": self.get_page_size(),
                    "offset": offset,
                    "searchText": ""
                }),
                callback=self.parse_list,
                dont_filter=True
            )

    def extract_job_urls(self, response) -> List[str]:
        data = response.json()
        jobs = data.get('jobPostings', [])
        base_url = "https://nvidia.wd5.myworkdayjobs.com/wday/cxs/nvidia/NVIDIAExternalCareerSite"
        
        urls = []
        for job in jobs:
            # 从 externalPath 构建完整的 URL
            if job.get('externalPath'):
                urls.append(f"{base_url}{job['externalPath']}")
        
        return urls

    def extract_job_data(self, response) -> JobItem:
        """从详情页提取工作信息"""
        data = response.json()
        job_info = data.get('jobPostingInfo', {})
        
        # 处理位置信息
        locations = []
        if job_info.get('location'):
            locations.append(job_info['location'])
        
        # 处理工作类型
        time_type = job_info.get('timeType', '')
        
        return JobItem(
            company_id=self.company.id,
            title=job_info.get('title', ''),
            url=job_info.get('externalUrl', response.url),
            full_description=self.sanitize_description(job_info.get('jobDescription', '')),
            raw_employment_type=time_type,
            raw_posted_date=job_info.get('startDate', None),
            locations=locations,
            expired=not job_info.get('canApply', True)
        )

    def skip_mark_expired(self) -> bool:
        return True
