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
    
    update_data = data.model_dump(exclude_unset=True)
    
    # Convert HttpUrl to string for storage
    for field in ["profile_image_url", "linkedin_url", "github_url", "twitter_url", "telegram_url", "calendly_url"]:
        if field in update_data and update_data[field]:
            update_data[field] = str(update_data[field])
    
    for field, value in update_data.items():
        setattr(profile, field, value)
    
    db.commit()
    db.refresh(profile)
    
    return profile