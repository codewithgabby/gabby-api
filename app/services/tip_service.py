from sqlalchemy.orm import Session
from app.models.tip import Tip
from app.schemas.tip import TipCreate, TipUpdate


def create_tip(db: Session, data: TipCreate):
    new_tip = Tip(
        title=data.title,
        category=data.category.value,
        content=data.content,
        summary=data.summary,
        telegram_link=data.telegram_link,
        is_published=data.is_published
    )
    
    db.add(new_tip)
    db.commit()
    db.refresh(new_tip)
    
    return new_tip


def get_all_tips(db: Session, category: str | None = None, published_only: bool = True):
    query = db.query(Tip)
    
    if published_only:
        query = query.filter(Tip.is_published == True)
    
    if category:
        query = query.filter(Tip.category == category)
    
    return query.order_by(Tip.created_at.desc()).all()


def get_tip_by_id(db: Session, tip_id: int):
    return db.query(Tip).filter(Tip.id == tip_id).first()


def update_tip(db: Session, tip_id: int, data: TipUpdate):
    tip = db.query(Tip).filter(Tip.id == tip_id).first()
    
    if not tip:
        return None
    
    update_data = data.model_dump(exclude_unset=True)
    
    # Convert enum to string value if category is being updated
    if "category" in update_data and update_data["category"]:
        update_data["category"] = update_data["category"].value
    
    for field, value in update_data.items():
        setattr(tip, field, value)
    
    db.commit()
    db.refresh(tip)
    
    return tip


def delete_tip(db: Session, tip_id: int):
    tip = db.query(Tip).filter(Tip.id == tip_id).first()
    
    if tip:
        tip.is_published = False  # Soft delete
        db.commit()
        db.refresh(tip)
    
    return tip


# Admin function to get ALL tips (including unpublished)
def get_all_tips_admin(db: Session, category: str | None = None):
    query = db.query(Tip)
    
    if category:
        query = query.filter(Tip.category == category)
    
    return query.order_by(Tip.created_at.desc()).all()