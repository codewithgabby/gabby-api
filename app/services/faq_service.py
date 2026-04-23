from sqlalchemy.orm import Session
from app.models.faq import FAQ
from app.schemas.faq import FAQCreate, FAQUpdate


def create_faq(db: Session, data: FAQCreate):
    new_faq = FAQ(
        question=data.question,
        answer=data.answer,
        category=data.category.value,
        display_order=data.display_order,
        telegram_link=data.telegram_link,
        is_published=data.is_published
    )
    
    db.add(new_faq)
    db.commit()
    db.refresh(new_faq)
    
    return new_faq

def get_all_faqs(db: Session, category: str | None = None, published_only: bool = True, page: int = 1, limit: int = 10):
    query = db.query(FAQ)
    
    if published_only:
        query = query.filter(FAQ.is_published == True)
    
    if category:
        query = query.filter(FAQ.category == category)
    
    return query.order_by(FAQ.display_order.asc(), FAQ.created_at.desc())\
        .offset((page - 1) * limit)\
        .limit(limit)\
        .all()

def get_faq_by_id(db: Session, faq_id: int):
    return db.query(FAQ).filter(FAQ.id == faq_id).first()


def update_faq(db: Session, faq_id: int, data: FAQUpdate):
    faq = db.query(FAQ).filter(FAQ.id == faq_id).first()
    
    if not faq:
        return None
    
    update_data = data.model_dump(exclude_unset=True)
    
    if "category" in update_data and update_data["category"]:
        update_data["category"] = update_data["category"].value
    
    for field, value in update_data.items():
        setattr(faq, field, value)
    
    db.commit()
    db.refresh(faq)
    
    return faq


def delete_faq(db: Session, faq_id: int):
    """Soft delete - sets is_published=False"""
    faq = db.query(FAQ).filter(FAQ.id == faq_id).first()
    
    if faq:
        faq.is_published = False
        db.commit()
        db.refresh(faq)
    
    return faq


def hard_delete_faq(db: Session, faq_id: int):
    """Hard delete - permanently removes from database"""
    faq = db.query(FAQ).filter(FAQ.id == faq_id).first()
    
    if faq:
        db.delete(faq)
        db.commit()
        return True
    
    return False


def get_all_faqs_admin(db: Session, category: str | None = None):
    query = db.query(FAQ)
    
    if category:
        query = query.filter(FAQ.category == category)
    
    return query.order_by(FAQ.display_order.asc(), FAQ.created_at.desc()).all()