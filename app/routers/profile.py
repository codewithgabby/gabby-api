from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.profile import ProfileUpdate, ProfileResponse
from app.services.profile_service import get_or_create_profile, update_profile
from app.dependencies import verify_admin, get_db

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/", response_model=ProfileResponse)
def get_profile(db: Session = Depends(get_db)):
    """Public: Get profile information"""
    return get_or_create_profile(db)


@router.put("/", response_model=ProfileResponse)
def update_profile_endpoint(
    data: ProfileUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(verify_admin)
):
    """Admin: Update profile information"""
    return update_profile(db, data)