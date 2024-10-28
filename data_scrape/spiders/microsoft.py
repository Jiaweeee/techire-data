import scrapy
from markdownify import markdownify as md
from data_scrape.items import JobItem
from data_storage.crud import CompanyCRUD
from typing import List

class MicrosoftSpider(scrapy.Spider):
    name = "microsoft"
    custom_settings = {
        'DOWNLOAD_DELAY': 0.3,
    }

    def __init__(self, *args, **kwargs):
        super(MicrosoftSpider, self).__init__(*args, **kwargs)
        self.company = CompanyCRUD().get_by_code(self.name)
        
    def start_requests(self):
        start_url = "https://gcsservices.careers.microsoft.com/search/api/v1/search"
        # 第一次请求获取总数
        yield scrapy.Request(url=start_url, callback=self.parse_first_page)

    def parse_first_page(self, response):
        data = response.json()
        total_jobs = data['operationResult']['result']['totalJobs']
        page_size = 20
        total_pages = total_jobs // page_size + (1 if total_jobs % page_size > 0 else 0)
        # 生成所有页面的请求
        for page in range(1, total_pages + 1):
            url = f"https://gcsservices.careers.microsoft.com/search/api/v1/search?pg={page}&pgSz={page_size}"
            yield scrapy.Request(url=url, callback=self.parse_list, dont_filter=True)

    def parse_list(self, response):
        data = response.json()
        jobs = data['operationResult']['result']['jobs']
        job_ids = [job['jobId'] for job in jobs]
        for job_id in job_ids:
            url = f"https://gcsservices.careers.microsoft.com/search/api/v1/job/{job_id}?lang=en_us"
            yield scrapy.Request(url=url, callback=self.parse_detail)

    def parse_detail(self, response):
        data = response.json()
        job_detail = data['operationResult']['result']
        posted_date = job_detail.get('posted') and job_detail['posted'].get('external')
        unposted = job_detail.get('unposted', None)
        expired = unposted is not None
        job_id = job_detail['jobId']
        detail_page_url = f"https://jobs.careers.microsoft.com/global/en/job/{job_id}"
        
        yield JobItem(
            company_id=self.company.id,
            title=job_detail['title'],
            url=detail_page_url,
            job_id=job_id,
            full_description=self._parse_job_description(job_detail),
            posted_date=posted_date,
            employment_type=job_detail['employmentType'],
            locations=self._parse_job_locations(job_detail),
            expired=expired
        )

    def _parse_job_description(self, job_detail: dict) -> str:
        description_html = job_detail['description']
        description_md ='## Overview\n' + self._html_to_markdown(description_html)
        qualifications_html = job_detail['qualifications']
        qualifications_md = '## Qualifications\n' + self._html_to_markdown(qualifications_html)
        responsibilities_html = job_detail['responsibilities']
        responsibilities_md = '## Responsibilities\n' + self._html_to_markdown(responsibilities_html)
        return description_md + '\n' + qualifications_md + '\n' + responsibilities_md

    def _parse_job_locations(self, job_detail: dict) -> List[str]:
        location_obj = job_detail['primaryWorkLocation']
        country = location_obj['country']
        state = location_obj['state']
        return [f"{country}, {state}"]

    def _html_to_markdown(self, html_text: str) -> str:
        return md(html_text)
    
