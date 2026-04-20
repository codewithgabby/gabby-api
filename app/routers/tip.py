from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.schemas.tip import TipCreate, TipUpdate, TipResponse
from app.services.tip_service import (
    create_tip,
    get_all_tips,
    get_tip_by_id,
    update_tip,
    delete_tip,
    get_all_tips_admin
)
from app.dependencies import verify_admin, get_db

router = APIRouter(prefix="/tips", tags=["Tips"])
limiter = Limiter(key_func=get_remote_address)


# PUBLIC ROUTES

@router.get("/", response_model=list[TipResponse])
def get_tips_public(
    request: Request,
    category: str | None = Query(None, description="Filter by: pr, visitor, study, general"),
    db: Session = Depends(get_db)
):
    """Public: Get all published tips, optionally filtered by category"""
    return get_all_tips(db, category=category, published_only=True)


@router.get("/{tip_id}", response_model=TipResponse)
def get_tip_public(tip_id: int, db: Session = Depends(get_db)):
    """Public: Get a single tip by ID (only if published)"""
    tip = get_tip_by_id(db, tip_id)
    
    if not tip:
        raise HTTPException(status_code=404, detail="Tip not found")
    
    if not tip.is_published:
        raise HTTPException(status_code=404, detail="Tip not found")
    
    return tip


# ADMIN ROUTES

@router.get("/admin/all", response_model=list[TipResponse])
def get_tips_admin(
    category: str | None = Query(None, description="Filter by: pr, visitor, study, general"),
    db: Session = Depends(get_db),
    _: str = Depends(verify_admin)
):
    """Admin: Get all tips (including unpublished)"""
    return get_all_tips_admin(db, category=category)


@router.post("/", response_model=TipResponse)
def create_tip_endpoint(
    data: TipCreate,
    db: Session = Depends(get_db),
    _: str = Depends(verify_admin)
):
    """Admin: Create a new tip"""
    return create_tip(db, data)


@router.put("/{tip_id}", response_model=TipResponse)
def update_tip_endpoint(
    tip_id: int,
    data: TipUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(verify_admin)
):
    """Admin: Update an existing tip"""
    tip = update_tip(db, tip_id, data)
    
    if not tip:
        raise HTTPException(status_code=404, detail="Tip not found")
    
    return tip


@router.delete("/{tip_id}")
def delete_tip_endpoint(
    tip_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(verify_admin)
):
    """Admin: Soft delete a tip (sets is_published=False)"""
    tip = delete_tip(db, tip_id)
    
    if not tip:
        raise HTTPException(status_code=404, detail="Tip not found")
    
    return {"message": f"Tip '{tip.title}' unpublished successfully"}