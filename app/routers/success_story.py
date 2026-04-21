from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.schemas.success_story import SuccessStoryCreate, SuccessStoryUpdate, SuccessStoryResponse
from app.services.success_story_service import (
    create_success_story,
    get_all_stories,
    get_featured_stories,
    get_story_by_id,
    update_story,
    delete_story,
    get_all_stories_admin,
    hard_delete_story
)
from app.dependencies import verify_admin, get_db

router = APIRouter(prefix="/success-stories", tags=["Success Stories"])


# PUBLIC ROUTES

@router.get("/", response_model=list[SuccessStoryResponse])
def get_stories_public(
    story_type: str | None = Query(None, description="Filter by: immigration, tech, consulting"),
    db: Session = Depends(get_db)
):
    """Public: Get all published success stories, optionally filtered by type"""
    return get_all_stories(db, story_type=story_type, published_only=True)


@router.get("/featured", response_model=list[SuccessStoryResponse])
def get_featured_stories_public(db: Session = Depends(get_db)):
    """Public: Get featured success stories (max 3)"""
    return get_featured_stories(db)


@router.get("/{story_id}", response_model=SuccessStoryResponse)
def get_story_public(story_id: int, db: Session = Depends(get_db)):
    """Public: Get a single success story by ID (only if published)"""
    story = get_story_by_id(db, story_id)
    
    if not story:
        raise HTTPException(status_code=404, detail="Success story not found")
    
    if not story.is_published:
        raise HTTPException(status_code=404, detail="Success story not found")
    
    return story


# ADMIN ROUTES

@router.get("/admin/all", response_model=list[SuccessStoryResponse])
def get_stories_admin(
    story_type: str | None = Query(None, description="Filter by: immigration, tech, consulting"),
    db: Session = Depends(get_db),
    _: str = Depends(verify_admin)
):
    """Admin: Get all success stories (including unpublished)"""
    return get_all_stories_admin(db, story_type=story_type)


@router.post("/", response_model=SuccessStoryResponse)
def create_story_endpoint(
    data: SuccessStoryCreate,
    db: Session = Depends(get_db),
    _: str = Depends(verify_admin)
):
    """Admin: Create a new success story"""
    return create_success_story(db, data)


@router.put("/{story_id}", response_model=SuccessStoryResponse)
def update_story_endpoint(
    story_id: int,
    data: SuccessStoryUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(verify_admin)
):
    """Admin: Update an existing success story"""
    story = update_story(db, story_id, data)
    
    if not story:
        raise HTTPException(status_code=404, detail="Success story not found")
    
    return story


@router.delete("/{story_id}")
def delete_story_endpoint(
    story_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(verify_admin)
):
    """Admin: HARD delete a success story (permanently removes from database)"""
    success = hard_delete_story(db, story_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Success story not found")
    
    return {"message": "Success story permanently deleted"}