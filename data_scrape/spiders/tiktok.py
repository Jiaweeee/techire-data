import scrapy
import json
from data_scrape.items import JobItem
from data_scrape.spiders.base import BasePagingJobSpider
from typing import List

class TiktokSpider(BasePagingJobSpider):
    name = "tiktok"
    
    def get_start_url(self) -> str:
        return "https://api.lifeattiktok.com/api/v1/public/supplier/search/job/posts"

    def get_total_jobs(self, response) -> int:
        data = response.json()
        return data['data']['count']

    def get_page_size(self) -> int:
        return 100  # Based on the limit in the request

    def get_page_url(self, page: int, page_size: int) -> str:
        # TikTok API uses POST request, this URL won't be used directly
        return self.get_start_url()

    def should_disable_filter(self) -> bool:
        return True

    def start_requests(self):
        """Override parent method to use POST request"""
        yield scrapy.Request(
            url=self.get_start_url(),
            method='POST',
            headers={
                'Website-Path': 'tiktok',
                'Content-Type': 'application/json'
            },
            body=json.dumps({
                "recruitment_id_list": [],
                "job_category_id_list": [],
                "subject_id_list": [],
                "location_code_list": [],
                "keyword": "",
                "limit": self.get_page_size(),
                "offset": 0
            }),
            callback=self.parse_first_page,
            dont_filter=True
        )

    def parse_first_page(self, response):
        """Handle first page and initiate subsequent requests"""
        total_jobs = self.get_total_jobs(response)
        self.total_jobs = total_jobs
        total_pages = (total_jobs + self.get_page_size() - 1) // self.get_page_size()
        
        # Handle first page data
        yield from self.parse_page(response)
        
        # Handle remaining pages
        for page in range(1, total_pages):
            offset = page * self.get_page_size()
            yield scrapy.Request(
                url=self.get_page_url(page, self.get_page_size()),
                method='POST',
                headers={
                    'Website-Path': 'tiktok',
                    'Content-Type': 'application/json'
                },
                body=json.dumps({
                    "recruitment_id_list": [],
                    "job_category_id_list": [],
                    "subject_id_list": [],
                    "location_code_list": [],
                    "keyword": "",
                    "limit": self.get_page_size(),
                    "offset": offset
                }),
                callback=self.parse_page,
                dont_filter=True,
                meta={'page': page}
            )

    def extract_job_urls(self, response) -> List[str]:
        # TikTok API returns complete job data, no need for separate URL list
        return []

    def extract_job_data(self, response) -> JobItem:
        # This method won't be called as we handle data directly in parse_page
        pass

    def parse_page(self, response):
        """Handle data from each page"""
        try:
            self.total_jobs = self.get_total_jobs(response)
            data = response.json()
            if not data or 'data' not in data or 'job_post_list' not in data['data']:
                self.logger.error(f"Invalid API response format: {data}")
                return

            jobs = data['data']['job_post_list']
            self.processed_jobs += len(jobs)
            for job in jobs:
                try:
                    job_item = self._parse_job_data(job)
                    self.active_job_urls.add(job_item.url)
                    yield job_item
                except Exception as e:
                    self.logger.error(f"Error processing job: {str(e)}")

            if self.processed_jobs >= self.total_jobs:
                self.crawl_successful = True
        except Exception as e:
            self.logger.error(f"Error processing page: {str(e)}")

    def _parse_job_data(self, job: dict) -> JobItem:
        """Parse individual job data"""
        location = []
        city_info = job.get('city_info', {})
        
        # Build location string from nested structure
        while city_info:
            if city_info.get('en_name'):
                location.insert(0, city_info['en_name'])
            city_info = city_info.get('parent')
        
        # Combine description and requirements into full_description
        full_description = job['description']
        if job.get('requirement'):
            full_description += "\n\nRequirements:\n" + job['requirement']
        
        return JobItem(
            company_id=self.company.id,
            title=job['title'],
            url=f"https://lifeattiktok.com/search/{job['id']}",
            full_description=self.sanitize_description(full_description, 'plaintext'),
            raw_employment_type="Full-time",  # All TikTok jobs are full-time
            locations=[', '.join(location)] if location else []
        ) 