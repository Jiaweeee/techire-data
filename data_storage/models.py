import uuid
from sqlalchemy import String, DateTime, ForeignKey, Boolean, Text, Integer, Float, ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship
from typing import Optional, Type, TypeVar, List
from datetime import datetime, timezone
from enum import Enum, IntEnum

T = TypeVar("T", bound="Base")

class Base(DeclarativeBase):
    """Base for all models."""
    
    id: Mapped[str] = mapped_column(
        String(64),
        primary_key=True,
        default=lambda _: str(uuid.uuid4()),
        unique=True,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    @classmethod
    def get(cls: Type[T], session: Session, id_: str) -> Optional[T]:
        return session.get(cls, id_)
    
    def save(self: T, session: Session) -> T:
        session.add(self)
        session.commit()
        session.refresh(self)
        return self
    
    def delete(self: T, session: Session) -> None:
        session.delete(self)
        session.commit()

class EmploymentType(int, Enum):
    FULL_TIME = 1
    PART_TIME = 2
    CONTRACT = 3
    INTERNSHIP = 4
    TEMPORARY = 5
    REMOTE = 6
    HYBRID = 7
    ON_SITE = 8

class ExperienceLevel(IntEnum):
    ENTRY = 1
    MID = 2
    SENIOR = 3
    LEAD = 4
    EXECUTIVE = 5

# define the Job model
class Job(Base):
    __tablename__ = 'jobs'
    
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    url: Mapped[str] = mapped_column(String(512), unique=True)
    full_description: Mapped[str] = mapped_column(Text, nullable=False)
    posted_date: Mapped[Optional[datetime]] = mapped_column(String(64), nullable=True, default=None)
    employment_type: Mapped[EmploymentType] = mapped_column(
        Integer,
        nullable=True,
        default=None
    )
    location: Mapped[str] = mapped_column(String(64), nullable=True, default=None)
    expired: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_remote: Mapped[bool] = mapped_column(Boolean, nullable=True, default=None)

    # Foreign key to company
    company_id: Mapped[str] = mapped_column(String(64), ForeignKey("companies.id"), nullable=False)
    # Relationship to company
    company: Mapped["Company"] = relationship("Company", back_populates="jobs")

    # Add this to existing Job model
    analysis: Mapped["JobAnalysis"] = relationship("JobAnalysis", back_populates="job", uselist=False)

# define the Company model
class Company(Base):
    __tablename__ = 'companies'
    
    code: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, comment="The unique code of the company")
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    official_site_url: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)
    careers_page_url: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)
    icon_url: Mapped[str] = mapped_column(String(512), nullable=False)
    introduction: Mapped[str] = mapped_column(Text, nullable=False)
    industry: Mapped[str] = mapped_column(String(64), nullable=True, default=None) # The industry where the company belongs to
    headquarters: Mapped[str] = mapped_column(String(64), nullable=True, default=None)
    
    # One-to-many relationship with jobs
    jobs: Mapped[List["Job"]] = relationship("Job", back_populates="company", cascade="all, delete-orphan")

class JobAnalysis(Base):
    __tablename__ = 'job_analyses'
    
    job_id: Mapped[str] = mapped_column(String(64), ForeignKey("jobs.id"), unique=True, nullable=False)
    job: Mapped["Job"] = relationship("Job", back_populates="analysis")
    
    status: Mapped[str] = mapped_column(
        String(32), 
        nullable=False, 
        default='pending', # pending, processing, completed, failed
        index=True
    )
    
    # Salary information
    salary_min: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    salary_max: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    salary_fixed: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    salary_currency: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    
    # Other extracted information
    skill_tags: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    experience_level: Mapped[Optional[ExperienceLevel]] = mapped_column(Integer, nullable=True)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
