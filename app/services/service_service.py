from sqlalchemy.orm import Session
from app.models.service import Service
from app.schemas.service import ServiceCreate


def create_service(db: Session, data: ServiceCreate):
    new_service = Service(
        name=data.name,
        category=data.category,
        description=data.description
    )

    db.add(new_service)
    db.commit()
    db.refresh(new_service)

    return new_service


def get_all_services(db: Session):
    return db.query(Service).filter(Service.is_active == True).all()


def delete_service(db: Session, service_id: int):
    service = db.query(Service).filter(Service.id == service_id).first()
    
    if service:
        service.is_active = False  # Soft delete
        db.commit()
        db.refresh(service)
    
    return service