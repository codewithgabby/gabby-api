from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.schemas.contact import ContactCreate, ContactResponse
from app.services.contact_service import create_contact, get_all_contacts, hard_delete_contact
from app.dependencies import verify_admin, get_db

router = APIRouter(prefix="/contact", tags=["Contact"])
limiter = Limiter(key_func=get_remote_address)


@router.post("/", response_model=ContactResponse)
@limiter.limit("5/hour")  # Max 5 contact submissions per hour per IP
def create_contact_endpoint(
    request: Request,
    contact: ContactCreate,
    db: Session = Depends(get_db)
):
    return create_contact(db, contact)


@router.get("/", response_model=list[ContactResponse])
def get_contacts(
    db: Session = Depends(get_db),
    _: str = Depends(verify_admin)
):
    return get_all_contacts(db)


@router.delete("/{contact_id}")
def delete_contact_endpoint(
    contact_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(verify_admin)
):
    """Admin: Permanently delete a contact message"""
    success = hard_delete_contact(db, contact_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    return {"message": "Contact message permanently deleted"}  