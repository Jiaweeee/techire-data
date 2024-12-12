import scrapy
import json
from data_scrape.items import JobItem
from data_scrape.spiders.base import BasePagingJobSpider
from typing import List

class UberSpider(BasePagingJobSpider):
    name = "uber"
    
    def get_start_url(self) -> str:
        return "https://www.uber.com/api/loadSearchJobsResults?localeCode=en"

    def get_total_jobs(self, response) -> int:
        data = response.json()
        return data['data']['totalResults']['low']

    def get_page_size(self) -> int:
        return 10

    def get_page_url(self, page: int, page_size: int) -> str:
        # Uber API 使用 POST 请求，这个 URL 不会被直接使用
        return "https://www.uber.com/api/loadSearchJobsResults?localeCode=en"

    def should_disable_filter(self) -> bool:
        return True

    def start_requests(self):
        """覆盖父类的方法，因为需要使用 POST 请求"""
        yield scrapy.Request(
            url=self.get_start_url(),
            method='POST',
            headers={
                'User-Agent': 'PostmanRuntime/7.43.0',
                'x-csrf-token': 'x',
                'Content-Type': 'application/json',
                'Cookie': '__cf_bm=owXcDpzrqhq8P0bgb21DEBuhM8rDXg2vv6ThX1juRU8-1733993149-1.0.1.1-J5Rym5sBdtV22z1XqTJtRlC7phafWh7ZUvmPXtKTL.NwWsQHfzOg4hlvNFJnH1hMP_tLAiTouf0LQ34yRqnCUQ; _ua={"session_id":"74e00138-0262-4bb8-906c-01f869a4d5fb","session_time_ms":1733971257237}; jwt-session=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InNsYXRlLWV4cGlyZXMtYXQiOjE3MzM5OTM1NTg1MDV9LCJpYXQiOjE3MzM5NzA5OTUsImV4cCI6MTczNDA1NzM5NX0.4ok6TGRIpexadS28lYb2uGrgMniAK8K099xwz0lqhIc; user_city_ids=965'
            },
            body=json.dumps({
                "limit": self.get_page_size(),
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
        total_jobs = self.get_total_jobs(response)
        total_pages = (total_jobs + self.get_page_size() - 1) // self.get_page_size()
        
        # 处理第一页数据
        yield from self.parse_page(response)
        
        # 处理剩余页面
        for page in range(1, total_pages):
            yield scrapy.Request(
                url=self.get_page_url(page, self.get_page_size()),
                method='POST',
                headers={
                    'x-csrf-token': 'x',
                    'Content-Type': 'application/json',
                },
                body=json.dumps({
                    "limit": self.get_page_size(),
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

    def extract_job_urls(self, response) -> List[str]:
        # Uber API 直接返回完整的工作数据，不需要单独的 URL 列表
        return []

    def extract_job_data(self, response) -> JobItem:
        # 这个方法不会被调用，因为我们直接在 parse_page 中处理数据
        pass

    def parse_page(self, response):
        """处理每一页的数据"""
        try:
            data = response.json()
            if not data or 'data' not in data or 'results' not in data['data']:
                self.logger.error(f"Invalid API response format: {data}")
                return

            jobs = data['data']['results']
            for job in jobs:
                try:
                    job_item = self._parse_job_data(job)
                    yield job_item
                except Exception as e:
                    self.logger.error(f"Error processing job: {str(e)}")

        except Exception as e:
            self.logger.error(f"Error processing page: {str(e)}")

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
            full_description=self.sanitize_description(job['description'], 'markdown'),
            raw_posted_date=job.get('creationDate'),
            raw_employment_type=job.get('timeType', ''),
            locations=locations,
            expired=job.get('statusName') != 'Approved'
        )