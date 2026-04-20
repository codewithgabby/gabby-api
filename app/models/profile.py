from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class Profile(Base):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False, default="Your Name")
    title = Column(String, nullable=False, default="Immigration Consultant & Software Engineer")
    bio = Column(Text, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    location = Column(String, nullable=True)
    profile_image_url = Column(String, nullable=True)
    linkedin_url = Column(String, nullable=True)
    github_url = Column(String, nullable=True)
    twitter_url = Column(String, nullable=True)
    telegram_url = Column(String, nullable=True)
    whatsapp_url = Column(String, nullable=True)
    calendly_url = Column(String, nullable=True)
    updated_at = Column(DateTime, onupdate=func.now())