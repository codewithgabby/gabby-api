from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class TipCategory(str, Enum):
    pr = "pr"
    visitor = "visitor"
    study = "study"
    general = "general"


class TipCreate(BaseModel):
    title: str
    category: TipCategory
    content: str
    summary: str | None = None
    telegram_link: str | None = None
    is_published: bool = True


class TipUpdate(BaseModel):
    title: str | None = None
    category: TipCategory | None = None
    content: str | None = None
    summary: str | None = None
    telegram_link: str | None = None
    is_published: bool | None = None


class TipResponse(BaseModel):
    id: int
    title: str
    category: str
    content: str
    summary: str | None
    telegram_link: str | None
    is_published: bool
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True