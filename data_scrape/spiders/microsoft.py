from data_scrape.spiders.base import BasePagingJobSpider
from typing import List

class MicrosoftSpider(BasePagingJobSpider):
    name = "microsoft"

    def get_start_url(self) -> str:
        return "https://gcsservices.careers.microsoft.com/search/api/v1/search"

    def get_total_jobs(self, response) -> int:
        data = response.json()
        return data['operationResult']['result']['totalJobs']

    def get_page_size(self) -> int:
        return 20

    def get_page_url(self, page: int, page_size: int) -> str:
        return f"https://gcsservices.careers.microsoft.com/search/api/v1/search?pg={page}&pgSz={page_size}"

    def should_disable_filter(self) -> bool:
        return True

    def extract_job_urls(self, response) -> List[str]:
        data = response.json()
        jobs = data['operationResult']['result']['jobs']
        return [f"https://gcsservices.careers.microsoft.com/search/api/v1/job/{job['jobId']}?lang=en_us" 
                for job in jobs]

    def extract_job_data(self, response) -> dict:
        data = response.json()
        job_detail = data['operationResult']['result']
        posted_date = job_detail.get('posted') and job_detail['posted'].get('external')
        unposted = job_detail.get('unposted', None)
        job_id = job_detail['jobId']
        
        return {
            'company_id': self.company.id,
            'title': job_detail['title'],
            'url': f"https://jobs.careers.microsoft.com/global/en/job/{job_id}",
            'job_id': job_id,
            'full_description': self._parse_job_description(job_detail),
            'posted_date': posted_date,
            'employment_type': job_detail['employmentType'],
            'locations': self._parse_job_locations(job_detail),
            'expired': unposted is not None
        }

    def _parse_job_description(self, job_detail: dict) -> str:
        description_md = '## Overview\n' + self._html_to_markdown(job_detail['description'])
        qualifications_md = '## Qualifications\n' + self._html_to_markdown(job_detail['qualifications'])
        responsibilities_md = '## Responsibilities\n' + self._html_to_markdown(job_detail['responsibilities'])
        return description_md + '\n' + qualifications_md + '\n' + responsibilities_md

    def _parse_job_locations(self, job_detail: dict) -> List[str]:
        location_obj = job_detail['primaryWorkLocation']
        country = location_obj['country']
        state = location_obj['state']
        return [f"{country}, {state}"]
    
