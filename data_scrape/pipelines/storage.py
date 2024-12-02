from data_storage.crud import JobCRUD, JobAnalysisCRUD
from data_scrape.items import JobItem
from data_storage.lib.normalizer import EmploymentTypeNormalizer, DateNormalizer


class JobInfoStoragePipeline:
    """
    Store the job info in the database
    """
    def __init__(self):
        self.job_crud = JobCRUD()
        self.job_analysis_crud = JobAnalysisCRUD()

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
            job = self.job_crud.create(
                title=item.title,
                url=item.url,
                full_description=item.full_description,
                company_id=item.company_id,
                job_id=item.job_id,
                posted_date=posted_date,
                employment_type=employment_type,
                location=', '.join(item.locations),
                expired=item.expired
            )
            # 创建初始状态为 pending 的 JobAnalysis 记录
            self.job_analysis_crud.create(
                job_id=job.id,
                status='pending'
            )
        


