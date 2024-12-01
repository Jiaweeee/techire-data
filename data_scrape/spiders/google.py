from data_scrape.spiders.base import BasePagingJobSpider
from typing import List

class GoogleSpider(BasePagingJobSpider):
    name = "google"

    def get_start_url(self) -> str:
        return "https://www.google.com/about/careers/applications/jobs/results"

    def get_total_jobs(self, response) -> int:
        total_jobs_str = response.xpath('//*[@id="yDmH0d"]/c-wiz[1]/div/div[2]/div/div/div[1]/div[1]/div/div[1]/div[1]/span/text()').get()
        return int(total_jobs_str.replace(',', ''))

    def get_page_size(self) -> int:
        return 20

    def get_page_url(self, page: int, page_size: int) -> str:
        return f"https://www.google.com/about/careers/applications/jobs/results?page={page}"

    def extract_job_urls(self, response) -> List[str]:
        items = response.xpath('//*[@id="yDmH0d"]/c-wiz[1]/div/div[2]/div/div/div[2]/main/div/c-wiz/div/ul/li').getall()
        urls = []
        for index in range(1, len(items) + 1):
            url = response.xpath(f'//*[@id="yDmH0d"]/c-wiz[1]/div/div[2]/div/div/div[2]/main/div/c-wiz/div/ul/li[{index}]/div/div/div[1]/div/div[5]/div/a/@href').get()
            url = response.urljoin(url).split('?')[0]
            urls.append(url)
        return urls

    def extract_job_data(self, response) -> dict:
        return {
            'company_id': self.company.id,
            'title': response.xpath('//*[@id="yDmH0d"]/c-wiz[1]/div/div[2]/div/div/div[2]/main/div/c-wiz/div/div/div/span/div/div[1]/h2/text()').get(),
            'url': response.url,
            'full_description': self._parse_full_description(response),
            'employment_type': "Full-time",  # All google jobs are full-time
            'locations': [response.xpath('//*[@id="yDmH0d"]/c-wiz[1]/div/div[2]/div/div/div[2]/main/div/c-wiz/div/div/div/span/div/div[2]/span[2]/span/text()').get()]
        }

    def _parse_full_description(self, response):
        full_html = ""
        # TODO: fix - some pages does not have all 3 divs
        for index in range(4, 7):
            html_text = response.xpath(f'//*[@id="yDmH0d"]/c-wiz[1]/div/div[2]/div/div/div[2]/main/div/c-wiz/div/div/div/span/div/div[{index}]').get()
            full_html += html_text
        return self.sanitize_html(full_html)