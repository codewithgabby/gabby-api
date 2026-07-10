from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class RedirectCreate(BaseModel):
    slug: str
    title: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    destination_url: str
    button_text: str = "Continue Reading"
    redirect_seconds: int = 5
    is_active: bool = True


class RedirectUpdate(BaseModel):
    slug: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    destination_url: Optional[str] = None
    button_text: Optional[str] = None
    redirect_seconds: Optional[int] = None
    is_active: Optional[bool] = None


class RedirectResponse(BaseModel):
    id: int
    slug: str
    title: str
    description: Optional[str]
    image_url: Optional[str]
    destination_url: str
    button_text: str
    redirect_seconds: int
    is_active: bool
    click_count: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True