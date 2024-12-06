from sqlalchemy.orm import Session, sessionmaker, joinedload
from typing import Optional, List, TypeVar, Generic, Type
from .models import Base, Company, Job, EmploymentType, JobAnalysis, ExperienceLevel
from .config import create_db_engine
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

T = TypeVar('T', bound=Base)


class BaseCRUD(Generic[T]):
    def __init__(self, model: Type[T]):
        engine = create_db_engine()
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        self.model = model

    def _get_session(self) -> Session:
        return self.SessionLocal()

    def create(self, **kwargs) -> T:
        obj = self.model(**kwargs)
        with self._get_session() as session:
            return obj.save(session)

    def get_by_id(self, id_: str) -> Optional[T]:
        with self._get_session() as session:
            return self.model.get(session, id_)
    
    def get_all(self, page: Optional[int] = None, page_size: Optional[int] = None) -> dict:
        """
        获取数据列表，支持分页
        :param page: 页码，从1开始。若为None则返回所有数据
        :param page_size: 每页数量。若为None则返回所有数据
        :return: 包含总数和数据列表的字典
        """
        with self._get_session() as session:
            # 构建查询
            query = session.query(self.model)
            
            # 如果提供了分页参数，则进行分页查询
            if page is not None and page_size is not None:
                offset = (page - 1) * page_size
                items = query.offset(offset).limit(page_size).all()
            else:
                items = query.all()
            return items
    
    def update(self, id_: str, **kwargs) -> Optional[T]:
        with self._get_session() as session:
            obj = self.model.get(session, id_)
            if not obj:
                return None
            
            for key, value in kwargs.items():
                if value is not None:
                    setattr(obj, key, value)
                    
            return obj.save(session)
    
    def delete(self, id_: str) -> bool:
        with self._get_session() as session:
            obj = self.model.get(session, id_)
            if not obj:
                return False
            obj.delete(session)
            return True


class CompanyCRUD(BaseCRUD[Company]):
    def __init__(self):
        super().__init__(Company)
    
    def get_by_code(self, code: str) -> Optional[Company]:
        with self._get_session() as session:
            return session.query(Company).filter(Company.code == code).first()
        
    def get_by_code_with_jobs(self, code: str) -> Optional[Company]:
        with self._get_session() as session:
            return session.query(Company).options(joinedload(Company.jobs)).filter(Company.code == code).first()
    
    def create(self, 
               code: str,
               name: str, 
               official_site_url: str,
               careers_page_url: str,
               icon_url: str,
               introduction: str,
               industry: Optional[str] = None,
               headquarters: Optional[str] = None) -> Company:
        return super().create(
            code=code,
            name=name,
            official_site_url=official_site_url,
            careers_page_url=careers_page_url,
            icon_url=icon_url,
            introduction=introduction,
            industry=industry,
            headquarters=headquarters
        )

class JobCRUD(BaseCRUD[Job]):
    def __init__(self):
        super().__init__(Job)
    
    def get_by_url(self, url: str) -> Optional[Job]:
        with self._get_session() as session:
            return session.query(Job).filter(Job.url == url).first()

    def create(self,
               title: str,
               url: str,
               full_description: str,
               company_id: str,
               posted_date: Optional[datetime] = None,
               employment_type: Optional[EmploymentType] = None,
               location: Optional[str] = None,
               expired: bool = False) -> Job:
        return super().create(
            title=title,
            url=url,
            full_description=full_description,
            company_id=company_id,
            posted_date=posted_date,
            employment_type=employment_type.value if employment_type else None,
            location=location,
            expired=expired
        )

    def mark_jobs_expired(self, company_id: str, active_job_urls: set[str]) -> int:
        """
        将不在 active_job_urls 中的工作标记为过期
        返回更新的记录数量
        """
        if not active_job_urls:  # 安全检查：如果活跃URL集合为空，不执行更新
            return 0
            
        with self._get_session() as session:
            result = session.query(Job).filter(
                Job.company_id == company_id,
                Job.expired == False,
                ~Job.url.in_(active_job_urls)
            ).update(
                {Job.expired: True}, 
                synchronize_session=False
            )
            session.commit()
            return result

class JobAnalysisCRUD(BaseCRUD[JobAnalysis]):
    def __init__(self):
        super().__init__(JobAnalysis)
    
    def create(self,
               job_id: str,
               status: str,
               salary_min: Optional[float] = None,
               salary_max: Optional[float] = None,
               salary_fixed: Optional[float] = None,
               salary_currency: Optional[str] = None,
               skill_tags: Optional[List[str]] = None,
               experience_level: Optional[ExperienceLevel] = None,
               summary: Optional[str] = None) -> JobAnalysis:
        return super().create(
            job_id=job_id,
            status=status,
            salary_min=salary_min,
            salary_max=salary_max,
            salary_fixed=salary_fixed,
            salary_currency=salary_currency,
            skill_tags=skill_tags,
            experience_level=experience_level.value if experience_level else None,
            summary=summary
        )

