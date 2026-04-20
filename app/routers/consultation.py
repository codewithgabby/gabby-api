from fastapi import APIRouter, Depends, Query, HTTPException, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.schemas.consultation import (
    ConsultationCreate,
    ConsultationResponse,
    ConsultationStatusUpdate
)
from app.services.consultation_service import (
    create_consultation,
    get_all_consultations,
    update_status
)
from app.dependencies import verify_admin, get_db

router = APIRouter(prefix="/consultations", tags=["Consultations"])
limiter = Limiter(key_func=get_remote_address)


@router.post("/", response_model=ConsultationResponse)
@limiter.limit("3/hour")  # Max 3 consultation requests per hour per IP
def create_consultation_endpoint(
    request: Request,
    data: ConsultationCreate,
    db: Session = Depends(get_db)
):
    return create_consultation(db, data)


@router.get("/", response_model=list[ConsultationResponse])
def get_consultations(
    status: str | None = Query(None, description="Filter by status: pending, approved, declined"),
    db: Session = Depends(get_db),
    _: str = Depends(verify_admin)
):
    return get_all_consultations(db, status)


@router.put("/{consultation_id}")
def update_consultation_status(
    consultation_id: int,
    status_update: ConsultationStatusUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(verify_admin)
):
    consultation = update_status(db, consultation_id, status_update.status.value)
    
    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation not found")
    
    return consultation