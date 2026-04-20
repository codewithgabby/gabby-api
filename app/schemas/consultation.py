from pydantic import BaseModel, EmailStr
from enum import Enum


class ConsultationCreate(BaseModel):
    name: str
    email: EmailStr
    service_type: str
    message: str | None = None


class ConsultationStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    declined = "declined"


class ConsultationStatusUpdate(BaseModel):
    status: ConsultationStatus


class ConsultationResponse(BaseModel):
    id: int
    name: str
    email: str
    service_type: str
    message: str | None
    status: str

    class Config:
        from_attributes = True