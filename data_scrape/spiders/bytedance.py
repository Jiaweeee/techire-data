import scrapy
import json
from data_scrape.items import JobItem
from data_scrape.spiders.base import BasePagingJobSpider
from typing import List

class ByteDanceSpider(BasePagingJobSpider):
    name = "bytedance"
    
    def get_start_url(self) -> str:
        return "https://jobs.bytedance.com/api/v1/search/job/posts"

    def get_total_jobs(self, response) -> int:
        data = response.json()
        return data['data']['count']

    def get_page_size(self) -> int:
        return 100

    def get_page_url(self, page: int, page_size: int) -> str:
        # ByteDance API uses POST request, this URL won't be used directly
        return self.get_start_url()

    def should_disable_filter(self) -> bool:
        return True

    def start_requests(self):
        """Override parent method to use POST request"""
        yield scrapy.Request(
            url=self.get_start_url(),
            method='POST',
            headers=self._get_headers(),
            body=json.dumps({
                "keyword": "",
                "limit": self.get_page_size(),
                "offset": 0,
                "job_category_id_list": [],
                "tag_id_list": [],
                "location_code_list": [],
                "subject_id_list": [],
                "recruitment_id_list": [],
                "portal_type": 4,
                "job_function_id_list": [],
                "portal_entrance": 1
            }),
            callback=self.parse_first_page,
            dont_filter=True
        )

    def _get_headers(self):
        return {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Cookie': 'ttwid=1%7Cxi4SHVMU6EbQHMkfs7jqRyMaWwHVPcdjqymb0_bv6x4%7C7C1718762270%7C7C697820f0ffae633f25913bf0c2367c9c7bb426fcf88fee2364a34c1063b961; locale=en-US; channel=overseas; platform=pc; s_v_web_id=verify_m4e4144n_dfGBiQVi_xGL0_4Vdm_8zT7_nyl08fyHn221; device-id=74456391446691249669; tea_uid=7445639144687322630',
            'Dnt': '1',
            'Env': 'undefined',
            'Host': 'jobs.bytedance.com',
            'Origin': 'https://jobs.bytedance.com',
            'Portal-Channel': 'overseas',
            'Portal-Platform': 'pc',
            'Referer': 'https://jobs.bytedance.com/en/position',
            'Sec-Ch-Ua': '"Chromium";v="131", "Not_A_Brand";v="24"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"macOS"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        }

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
                headers=self._get_headers(),
                body=json.dumps({
                    "keyword": "",
                    "limit": self.get_page_size(),
                    "offset": offset,
                    "job_category_id_list": [],
                    "tag_id_list": [],
                    "location_code_list": [],
                    "subject_id_list": [],
                    "recruitment_id_list": [],
                    "portal_type": 4,
                    "job_function_id_list": [],
                    "portal_entrance": 1
                }),
                callback=self.parse_page,
                dont_filter=True,
                meta={'page': page}
            )

    def extract_job_urls(self, response) -> List[str]:
        # ByteDance API returns complete job data, no need for separate URL list
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
        # Extract locations from city_list
        locations = []
        city_list = job.get('city_list', [])
        for city in city_list:
            location_parts = []
            if city.get('en_name'):
                location_parts.append(city['en_name'])
            if location_parts:
                locations.append(', '.join(location_parts))

        # Combine description and requirement
        full_description = job.get('description', '')
        if job.get('requirement'):
            full_description += "\n\nRequirements:\n" + job['requirement']

        return JobItem(
            company_id=self.company.id,
            title=job['title'],
            url=f"https://jobs.bytedance.com/en/position/{job['id']}/detail",
            full_description=self.sanitize_description(full_description, 'plaintext'),
            raw_employment_type='Full-time',  # All bytedance jobs are full-time
            raw_posted_date=job.get('publish_time'),
            locations=locations  # 使用新解析的locations列表
        )
