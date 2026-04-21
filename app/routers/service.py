from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.service import Service

from app.schemas.service import ServiceCreate, ServiceUpdate, ServiceResponse
from app.services.service_service import create_service, get_all_services, delete_service
from app.dependencies import verify_admin, get_db

router = APIRouter(prefix="/services", tags=["Services"])


@router.post("/", response_model=ServiceResponse)
def create_service_endpoint(
    data: ServiceCreate,
    db: Session = Depends(get_db),
    _: str = Depends(verify_admin)
):
    return create_service(db, data)


@router.get("/", response_model=list[ServiceResponse])
def get_services(db: Session = Depends(get_db)):
    return get_all_services(db)


@router.get("/{service_id}", response_model=ServiceResponse)
def get_service(service_id: int, db: Session = Depends(get_db)):
    """Public: Get a single service by ID"""
    service = db.query(Service).filter(Service.id == service_id, Service.is_active == True).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service


@router.put("/{service_id}", response_model=ServiceResponse)
def update_service_endpoint(
    service_id: int,
    data: ServiceUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(verify_admin)
):
    """Admin: Update a service (partial updates allowed)"""
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(service, field, value)
    
    db.commit()
    db.refresh(service)
    return service


@router.delete("/{service_id}")
def delete_service_endpoint(
    service_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(verify_admin)
):
    service = delete_service(db, service_id)
    
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    return {"message": f"Service '{service.name}' deleted successfully"}