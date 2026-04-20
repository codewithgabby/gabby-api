from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class FAQCategory(str, Enum):
    pr = "pr"
    study = "study"
    visitor = "visitor"
    settlement = "settlement"


class FAQCreate(BaseModel):
    question: str
    answer: str
    category: FAQCategory
    display_order: int = 0
    telegram_link: str | None = None
    is_published: bool = True


class FAQUpdate(BaseModel):
    question: str | None = None
    answer: str | None = None
    category: FAQCategory | None = None
    display_order: int | None = None
    telegram_link: str | None = None
    is_published: bool | None = None


class FAQResponse(BaseModel):
    id: int
    question: str
    answer: str
    category: str
    display_order: int
    telegram_link: str | None
    is_published: bool
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True