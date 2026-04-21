from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional


class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    title: Optional[str] = None
    bio: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    profile_image_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    twitter_url: Optional[str] = None
    telegram_url: Optional[str] = None
    whatsapp_url: Optional[str] = None
    calendly_url: Optional[str] = None

    @field_validator('profile_image_url', 'linkedin_url', 'github_url', 'twitter_url', 'telegram_url', 'calendly_url', mode='before')
    @classmethod
    def empty_str_to_none(cls, v):
        """Convert empty strings to None for URL fields"""
        if v == "" or v is None:
            return None
        return v


class ProfileResponse(BaseModel):
    id: int
    full_name: str
    title: str
    bio: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    profile_image_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    twitter_url: Optional[str] = None
    telegram_url: Optional[str] = None
    whatsapp_url: Optional[str] = None
    calendly_url: Optional[str] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True