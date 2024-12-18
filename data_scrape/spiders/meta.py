from data_scrape.spiders.base import BasePagingJobSpider
from typing import List
from data_scrape.items import JobItem
import scrapy


class MetaSpider(BasePagingJobSpider):
    name = "meta"
    
    def get_start_url(self) -> str:
        return "https://www.metacareers.com/graphql"

    def get_total_jobs(self, response) -> int:
        data = response.json()
        return len(data['data']['job_search'])

    def get_page_size(self) -> int:
        # Meta API returns all jobs in one request
        return 1000

    def get_page_url(self, page: int, page_size: int) -> str:
        return self.get_start_url()

    def should_disable_filter(self) -> bool:
        return True

    def start_requests(self):
        """Override parent method to use POST request with required payload"""
        yield scrapy.Request(
            url=self.get_start_url(),
            method='POST',
            headers = {
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'application/x-www-form-urlencoded',
                'cookie': 'datr=YmgOZ9zFeFYN70B8jE-5iaF1; ps_l=1; ps_n=1; wd=1023x1035',
                'dnt': '1',
                'origin': 'https://www.metacareers.com',
                'priority': 'u=1, i',
                'referer': 'https://www.metacareers.com/jobs',
                'sec-ch-ua': '"Chromium";v="131", "Not_A Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
                'x-asbd-id': '129477',
                'x-fb-friendly-name': 'CareersJobSearchResultsQuery',
                'x-fb-lsd': 'AVpDP_BJ2i4'
            },
            body='av=0&__user=0&__a=1&__req=2&__hs=20075.BP%3ADEFAULT.2.0.0.0.0&dpr=2&__ccg=EXCELLENT&__rev=1018959383&__s=4zfoxf%3A9wwyut%3Ayzv30a&__hsi=7449678358878798677&__dyn=7xeUmwkHg7ebwKBAg5S1Dxu13wqovzEdEc8uxa1twKzobo1nEhwem0nCq1ewcG0RU2Cwooa81VohwnU14E9k2C0sy0H82NxCawcK1iwmE2ewnE2Lw5XwSyES4E3PwbS1Lwqo3cwbq0x8qw53wtU5K0zU5a&__csr=&lsd=AVpDP_BJ2i4&jazoest=2853&__spin_r=1018959383&__spin_b=trunk&__spin_t=1734513407&__jssesw=1&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=CareersJobSearchResultsQuery&variables=%7B%22search_input%22%3A%7B%22q%22%3Anull%2C%22divisions%22%3A%5B%5D%2C%22offices%22%3A%5B%5D%2C%22roles%22%3A%5B%5D%2C%22leadership_levels%22%3A%5B%5D%2C%22saved_jobs%22%3A%5B%5D%2C%22saved_searches%22%3A%5B%5D%2C%22sub_teams%22%3A%5B%5D%2C%22teams%22%3A%5B%5D%2C%22is_leadership%22%3Afalse%2C%22is_remote_only%22%3Afalse%2C%22sort_by_new%22%3Afalse%2C%22results_per_page%22%3Anull%7D%7D&server_timestamps=true&doc_id=9114524511922157',
            callback=self.parse_first_page,
            dont_filter=True
        )

    def extract_job_urls(self, response) -> List[str]:
        # Meta API returns complete job data, no need for separate URL list
        return []

    def extract_job_data(self, response) -> JobItem:
        title = response.meta['title']
        locations = response.meta['locations']
        
        description = response.xpath('//*[@id="careersContentContainer"]/div/div[3]/div[2]/div/div/div[1]').get()
        
        return JobItem(
            company_id=self.company.id,
            title=title,
            url=response.url,
            full_description=self.sanitize_description(description),
            locations=locations
        )

    def parse_first_page(self, response):
        """Handle first page and extract job URLs"""
        self.total_jobs = self.get_total_jobs(response)
        data = response.json()
        jobs = data['data']['job_search']
        
        self.active_job_urls.update(
            f"https://www.metacareers.com/jobs/{job['id']}" 
            for job in jobs
        )
        self.processed_jobs = len(jobs)
        
        for job in jobs:
            url = f"https://www.metacareers.com/jobs/{job['id']}"
            yield scrapy.Request(
                url=url,
                callback=self.parse_detail,
                dont_filter=True,
                meta={
                    'title': job['title'],
                    'locations': job['locations']
                }
            )
        
        if self.processed_jobs >= self.total_jobs:
            self.crawl_successful = True
