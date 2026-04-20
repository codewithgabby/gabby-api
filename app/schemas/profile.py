from pydantic import BaseModel, HttpUrl, EmailStr
from datetime import datetime

class ProfileUpdate(BaseModel):
    full_name: str | None = None
    title: str | None = None
    bio: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    location: str | None = None
    profile_image_url: HttpUrl | None = None
    linkedin_url: HttpUrl | None = None
    github_url: HttpUrl | None = None
    twitter_url: HttpUrl | None = None
    telegram_url: HttpUrl | None = None
    whatsapp_url: str | None = None  # wa.me links
    calendly_url: HttpUrl | None = None


class ProfileResponse(BaseModel):
    id: int
    full_name: str
    title: str
    bio: str | None
    email: str | None
    phone: str | None
    location: str | None
    profile_image_url: str | None
    linkedin_url: str | None
    github_url: str | None
    twitter_url: str | None
    telegram_url: str | None
    whatsapp_url: str | None
    calendly_url: str | None
    updated_at: datetime | None

    class Config:
        from_attributes = True