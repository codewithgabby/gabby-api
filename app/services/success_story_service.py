from sqlalchemy.orm import Session
from app.models.success_story import SuccessStory
from app.schemas.success_story import SuccessStoryCreate, SuccessStoryUpdate


def create_success_story(db: Session, data: SuccessStoryCreate):
    new_story = SuccessStory(
        client_name=data.client_name,
        client_country=data.client_country,
        story_type=data.story_type.value,
        outcome=data.outcome,
        quote=data.quote,
        image_url=str(data.image_url) if data.image_url else None,
        linkedin_url=str(data.linkedin_url) if data.linkedin_url else None,
        is_featured=data.is_featured,
        is_published=data.is_published
    )
    
    db.add(new_story)
    db.commit()
    db.refresh(new_story)
    
    return new_story


def get_all_stories(db: Session, story_type: str | None = None, published_only: bool = True):
    query = db.query(SuccessStory)
    
    if published_only:
        query = query.filter(SuccessStory.is_published == True)
    
    if story_type:
        query = query.filter(SuccessStory.story_type == story_type)
    
    return query.order_by(SuccessStory.is_featured.desc(), SuccessStory.created_at.desc()).all()


def get_featured_stories(db: Session, limit: int = 3):
    return db.query(SuccessStory)\
        .filter(SuccessStory.is_published == True, SuccessStory.is_featured == True)\
        .order_by(SuccessStory.created_at.desc())\
        .limit(limit)\
        .all()


def get_story_by_id(db: Session, story_id: int):
    return db.query(SuccessStory).filter(SuccessStory.id == story_id).first()


def update_story(db: Session, story_id: int, data: SuccessStoryUpdate):
    story = db.query(SuccessStory).filter(SuccessStory.id == story_id).first()
    
    if not story:
        return None
    
    update_data = data.model_dump(exclude_unset=True)
    
    if "story_type" in update_data and update_data["story_type"]:
        update_data["story_type"] = update_data["story_type"].value
    
    if "image_url" in update_data and update_data["image_url"]:
        update_data["image_url"] = str(update_data["image_url"])
    
    if "linkedin_url" in update_data and update_data["linkedin_url"]:
        update_data["linkedin_url"] = str(update_data["linkedin_url"])
    
    for field, value in update_data.items():
        setattr(story, field, value)
    
    db.commit()
    db.refresh(story)
    
    return story


def delete_story(db: Session, story_id: int):
    """Soft delete - sets is_published=False"""
    story = db.query(SuccessStory).filter(SuccessStory.id == story_id).first()
    
    if story:
        story.is_published = False
        db.commit()
        db.refresh(story)
    
    return story


def hard_delete_story(db: Session, story_id: int):
    """Hard delete - permanently removes from database"""
    story = db.query(SuccessStory).filter(SuccessStory.id == story_id).first()
    
    if story:
        db.delete(story)
        db.commit()
        return True
    
    return False


def get_all_stories_admin(db: Session, story_type: str | None = None):
    query = db.query(SuccessStory)
    
    if story_type:
        query = query.filter(SuccessStory.story_type == story_type)
    
    return query.order_by(SuccessStory.created_at.desc()).all()