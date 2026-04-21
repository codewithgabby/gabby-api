from sqlalchemy.orm import Session
from app.models.profile import Profile
from app.schemas.profile import ProfileUpdate


def get_or_create_profile(db: Session) -> Profile:
    """Returns the single profile row. Creates it if it doesn't exist."""
    profile = db.query(Profile).first()
    
    if not profile:
        profile = Profile()
        db.add(profile)
        db.commit()
        db.refresh(profile)
    
    return profile


def update_profile(db: Session, data: ProfileUpdate) -> Profile:
    profile = get_or_create_profile(db)
    
    # Only update fields that were actually sent
    update_data = data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(profile, field, value)
    
    db.commit()
    db.refresh(profile)
    
    return profile