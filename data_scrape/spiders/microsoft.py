from data_scrape.spiders.base import BasePagingJobSpider
from typing import List
from data_scrape.items import JobItem
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

    def extract_job_data(self, response) -> JobItem:
        data = response.json()
        job_detail = data['operationResult']['result']
        posted_date = job_detail.get('posted') and job_detail['posted'].get('external')
        unposted = job_detail.get('unposted', None)
        job_id = job_detail['jobId']
        
        return JobItem(
            company_id=self.company.id,
            title=job_detail['title'],
            url=f"https://jobs.careers.microsoft.com/global/en/job/{job_id}",
            full_description=self._parse_job_description(job_detail),
            raw_posted_date=posted_date,
            raw_employment_type=job_detail['employmentType'],
            locations=self._parse_job_locations(job_detail),
            expired=unposted is not None
        )
    
    def skip_mark_expired(self) -> bool:
        return True

    def _parse_job_description(self, job_detail: dict) -> str:
        sections = [
            ('Overview', job_detail.get('description')),
            ('Qualifications', job_detail.get('qualifications')),
            ('Responsibilities', job_detail.get('responsibilities'))
        ]
        
        # 使用统一的 HTML 结构
        return '\n'.join(
            f'<section>'
            f'<h2>{title}</h2>'
            f'{self.sanitize_description(content)}'
            f'</section>'
            for title, content in sections
        )

    def _parse_job_locations(self, job_detail: dict) -> List[str]:
        def _format_location(loc: dict) -> str:
            city = loc.get('city', '')
            state = loc.get('state', '')
            country = loc.get('country', '')
            if city and state and country:
                return f"{city}, {state}, {country}"
            elif state and country:
                return f"{state}, {country}"
            return ''
        
        locations = []
        
        # 处理 primaryWorkLocation
        primary_loc = job_detail.get('primaryWorkLocation')
        if primary_loc:
            location = _format_location(primary_loc)
            if location:
                locations.append(location)
        
        # 处理 workLocations
        for loc in job_detail.get('workLocations', []):
            location = _format_location(loc)
            if location:
                locations.append(location)
        
        return list(set(locations))
    
