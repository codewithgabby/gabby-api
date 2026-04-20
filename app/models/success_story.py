from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class SuccessStory(Base):
    __tablename__ = "success_stories"

    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String, nullable=False)  # First name only
    client_country = Column(String, nullable=False)  # "Nigeria → Canada"
    story_type = Column(String, nullable=False)  # immigration, tech, consulting
    outcome = Column(String, nullable=False)  # "Got PR in 4 months"
    quote = Column(Text, nullable=False)
    image_url = Column(String, nullable=True)
    linkedin_url = Column(String, nullable=True)
    is_featured = Column(Boolean, default=False)
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())