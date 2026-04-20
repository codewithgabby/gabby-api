from sqlalchemy import Column, Integer, String, Text
from app.db.base import Base


class Consultation(Base):
    __tablename__ = "consultations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    service_type = Column(String, nullable=False)
    message = Column(Text, nullable=True)
    status = Column(String, default="pending")