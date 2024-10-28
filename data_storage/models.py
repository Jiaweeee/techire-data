import uuid
from sqlalchemy import String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship
from typing import Optional, Type, TypeVar, List
from datetime import datetime, timezone

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

# define the Job model
class Job(Base):
    __tablename__ = 'jobs'
    
    title: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String, unique=True)
    full_description: Mapped[str] = mapped_column(String)
    job_id: Mapped[str] = mapped_column(String(64), nullable=True, default=None)
    posted_date: Mapped[str] = mapped_column(String, nullable=True, default=None)
    employment_type: Mapped[str] = mapped_column(String, nullable=True, default=None)
    location: Mapped[str] = mapped_column(String, nullable=True, default=None)
    skill_tags: Mapped[str] = mapped_column(String, nullable=True, default=None)
    salary_range: Mapped[str] = mapped_column(String, nullable=True, default=None)
    expired: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # Foreign key to company
    company_id: Mapped[str] = mapped_column(String(64), ForeignKey("companies.id"), nullable=False)
    # Relationship to company
    company: Mapped["Company"] = relationship("Company", back_populates="jobs")

# define the Company model
class Company(Base):
    __tablename__ = 'companies'
    
    code: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, comment="The unique code of the company")
    name: Mapped[str] = mapped_column(String, nullable=False)
    official_site_url: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    careers_page_url: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    icon_url: Mapped[str] = mapped_column(String, nullable=False)
    introduction: Mapped[str] = mapped_column(String, nullable=False)
    industry: Mapped[str] = mapped_column(String, nullable=True, default=None) # The industry where the company belongs to
    headquarters: Mapped[str] = mapped_column(String, nullable=True, default=None)
    
    # One-to-many relationship with jobs
    jobs: Mapped[List["Job"]] = relationship("Job", back_populates="company", cascade="all, delete-orphan")
