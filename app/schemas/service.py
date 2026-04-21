from pydantic import BaseModel
from typing import Optional


class ServiceCreate(BaseModel):
    name: str
    category: str
    description: str


class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None


class ServiceResponse(BaseModel):
    id: int
    name: str
    category: str
    description: str
    is_active: bool

    class Config:
        from_attributes = True