from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class Redirect(Base):
    __tablename__ = "redirects"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, nullable=False, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    destination_url = Column(String, nullable=False)
    button_text = Column(String, default="Continue Reading")
    redirect_seconds = Column(Integer, default=5)
    is_active = Column(Boolean, default=True)
    click_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())