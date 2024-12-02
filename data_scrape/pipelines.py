# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from data_storage.crud import JobCRUD
from data_scrape.items import JobItem
from data_storage.lib.normalizer import EmploymentTypeNormalizer, DateNormalizer

class JobInfoExtractionPipeline:
    """
    Extract useful information from the job description using AI
    """
    def process_item(self, item: JobItem, spider):
        # TODO
        pass


class JobInfoStoragePipeline:
    """
    Store the job info in the database
    """
    def __init__(self):
        self.job_crud = JobCRUD()

    def process_item(self, item: JobItem, spider):
        # Normalization
        employment_type = EmploymentTypeNormalizer.normalize(item.raw_employment_type)
        posted_date = DateNormalizer.normalize(item.raw_posted_date)

        # Store job info
        job = self.job_crud.get_by_url(item.url)
        # If job exists, update expired info
        if job:
            if job.expired != item.expired:
                self.job_crud.update(job.id, expired=item.expired)
        else:
            self.job_crud.create(
                title=item.title,
                url=item.url,
                full_description=item.full_description,
                company_id=item.company_id,
                job_id=item.job_id,
                posted_date=posted_date,
                employment_type=employment_type,
                location=', '.join(item.locations),
                skill_tags=', '.join(item.skill_tags),
                salary_range=item.salary_range,
                expired=item.expired
            )
        


