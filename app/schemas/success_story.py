from pydantic import BaseModel, HttpUrl
from datetime import datetime
from enum import Enum


class StoryType(str, Enum):
    immigration = "immigration"
    tech = "tech"
    consulting = "consulting"


class SuccessStoryCreate(BaseModel):
    client_name: str
    client_country: str
    story_type: StoryType
    outcome: str
    quote: str
    image_url: HttpUrl | None = None
    linkedin_url: HttpUrl | None = None
    is_featured: bool = False
    is_published: bool = True


class SuccessStoryUpdate(BaseModel):
    client_name: str | None = None
    client_country: str | None = None
    story_type: StoryType | None = None
    outcome: str | None = None
    quote: str | None = None
    image_url: HttpUrl | None = None
    linkedin_url: HttpUrl | None = None
    is_featured: bool | None = None
    is_published: bool | None = None


class SuccessStoryResponse(BaseModel):
    id: int
    client_name: str
    client_country: str
    story_type: str
    outcome: str
    quote: str
    image_url: str | None
    linkedin_url: str | None
    is_featured: bool
    is_published: bool
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True