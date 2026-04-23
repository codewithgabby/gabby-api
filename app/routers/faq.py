from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.schemas.faq import FAQCreate, FAQUpdate, FAQResponse
from app.services.faq_service import (
    create_faq,
    get_all_faqs,
    get_faq_by_id,
    update_faq,
    delete_faq,
    get_all_faqs_admin,
    hard_delete_faq
)
from app.dependencies import verify_admin, get_db

router = APIRouter(prefix="/faqs", tags=["FAQ"])
limiter = Limiter(key_func=get_remote_address)


# PUBLIC ROUTES

@router.get("/", response_model=list[FAQResponse])
def get_faqs_public(
    request: Request,
    category: str | None = Query(None, description="Filter by: pr, study, visitor, settlement"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=50, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Public: Get published FAQs with pagination and filtering"""
    return get_all_faqs(db, category=category, page=page, limit=limit, published_only=True)

# ADMIN ROUTES

@router.get("/admin/all", response_model=list[FAQResponse])
def get_faqs_admin(
    category: str | None = Query(None, description="Filter by: pr, study, visitor, settlement"),
    db: Session = Depends(get_db),
    _: str = Depends(verify_admin)
):
    """Admin: Get all FAQs (including unpublished)"""
    return get_all_faqs_admin(db, category=category)


@router.get("/{faq_id}", response_model=FAQResponse)
def get_faq_by_id_endpoint(
    faq_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(verify_admin)
):
    """Admin: Get a single FAQ by ID (for editing)"""
    faq = get_faq_by_id(db, faq_id)
    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")
    return faq


@router.post("/", response_model=FAQResponse)
def create_faq_endpoint(
    data: FAQCreate,
    db: Session = Depends(get_db),
    _: str = Depends(verify_admin)
):
    """Admin: Create a new FAQ"""
    return create_faq(db, data)


@router.put("/{faq_id}", response_model=FAQResponse)
def update_faq_endpoint(
    faq_id: int,
    data: FAQUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(verify_admin)
):
    """Admin: Update an existing FAQ"""
    faq = update_faq(db, faq_id, data)
    
    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")
    
    return faq


@router.delete("/{faq_id}")
def delete_faq_endpoint(
    faq_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(verify_admin)
):
    """Admin: HARD delete an FAQ (permanently removes from database)"""
    success = hard_delete_faq(db, faq_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="FAQ not found")
    
    return {"message": f"FAQ permanently deleted"}