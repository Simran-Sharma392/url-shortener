from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.database import Base

class URL(Base):
    __tablename__="urls"
    id = Column(Integer, primary_key=True)
    original_url = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=func.now())
    access_count = Column(Integer, default=0)
    clicks=relationship("Click", back_populates="url", cascade="all, delete-orphan")

class Click(Base):
    __tablename__="clicks"
    id=Column(Integer, primary_key=True)
    url_id=Column(Integer, ForeignKey("urls.id"))
    timestamp=Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    user_agent=Column(String)
    url=relationship("URL", back_populates="clicks")

    