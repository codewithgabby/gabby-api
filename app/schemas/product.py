from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str
    link: str
    type: str


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    link: str
    type: str
    is_active: bool

    class Config:
        from_attributes = True