from sqlalchemy.orm import Session, sessionmaker, joinedload
from typing import Optional, List, TypeVar, Generic, Type
from .models import Base, Company, Job
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
    
    def get_all(self) -> List[T]:
        with self._get_session() as session:
            return session.query(self.model).all()
    
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
               job_id: Optional[str] = None,
               posted_date: Optional[str] = None,
               normalized_posted_date: Optional[datetime] = None,
               employment_type: Optional[str] = None,
               normalized_employment_type: Optional[str] = None,
               location: Optional[str] = None,
               skill_tags: Optional[str] = None,
               salary_range: Optional[str] = None,
               expired: bool = False) -> Job:
        return super().create(
            title=title,
            url=url,
            full_description=full_description,
            company_id=company_id,
            job_id=job_id,
            posted_date=posted_date,
            normalized_posted_date=normalized_posted_date,
            employment_type=employment_type,
            normalized_employment_type=normalized_employment_type,
            location=location,
            skill_tags=skill_tags,
            salary_range=salary_range,
            expired=expired
        )

