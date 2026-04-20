from pydantic import BaseModel


class ServiceCreate(BaseModel):
    name: str
    category: str
    description: str


class ServiceResponse(BaseModel):
    id: int
    name: str
    category: str
    description: str
    is_active: bool

    class Config:
        from_attributes = True