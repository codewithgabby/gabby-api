from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.models.tip import Tip

from app.schemas.tip import TipCreate, TipUpdate, TipResponse
from app.services.tip_service import (
    create_tip,
    get_all_tips,
    get_tip_by_id,
    update_tip,
    delete_tip,
    hard_delete_tip
)
from app.dependencies import verify_admin, get_db

router = APIRouter(prefix="/tips", tags=["Tips"])
limiter = Limiter(key_func=get_remote_address)


# PUBLIC ROUTES

@router.get("/", response_model=list[TipResponse])
def get_tips_public(
    request: Request,
    category: str | None = Query(None, description="Filter by: pr, visitor, study, general"),
    search: str | None = Query(None, description="Search in title, summary, and content"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(6, ge=1, le=50, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Public: Get published tips with pagination, filtering, and search"""
    query = db.query(Tip).filter(Tip.is_published == True)
    
    if category:
        query = query.filter(Tip.category == category)
    
    # Search in title, summary, and content
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            Tip.title.ilike(search_term) | 
            Tip.summary.ilike(search_term) |
            Tip.content.ilike(search_term)
        )
    
    total = query.count()
    tips = query.order_by(Tip.created_at.desc()).offset((page - 1) * limit).limit(limit).all()
    
    return tips

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
    category: str | None = Query(None, description="Filter by category"),
    status: str | None = Query(None, description="Filter by status: published, draft"),
    search: str | None = Query(None, description="Search in title, summary, and content"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=50, description="Items per page"),
    db: Session = Depends(get_db),
    _: str = Depends(verify_admin)
):
    """Admin: Get tips with filtering, search, and pagination"""
    query = db.query(Tip)
    
    # Filter by category
    if category and category != "all":
        query = query.filter(Tip.category == category)
    
    # Filter by status
    if status and status != "all":
        is_published = status == "published"
        query = query.filter(Tip.is_published == is_published)
    
    # Search in title and summary
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            Tip.title.ilike(search_term) | 
            Tip.summary.ilike(search_term)
        )
    
    # Get total count
    total = query.count()
    
    # Paginate
    tips = query.order_by(Tip.created_at.desc())\
        .offset((page - 1) * limit)\
        .limit(limit)\
        .all()
    
    return tips


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
    """Admin: HARD delete a tip (permanently removes from database)"""
    success = hard_delete_tip(db, tip_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Tip not found")
    
    return {"message": "Tip permanently deleted"}