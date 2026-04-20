from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class Tip(Base):
    __tablename__ = "tips"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)  # pr, visitor, study, general
    content = Column(Text, nullable=False)
    summary = Column(String(200), nullable=True)  # Short preview for listings
    telegram_link = Column(String, nullable=True)  # Link to your DIY group post
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())