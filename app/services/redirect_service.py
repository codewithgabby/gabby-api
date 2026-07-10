from sqlalchemy.orm import Session
from app.models.redirect import Redirect
from app.schemas.redirect import RedirectCreate, RedirectUpdate


def create_redirect(db: Session, data: RedirectCreate):
    new_redirect = Redirect(
        slug=data.slug,
        title=data.title,
        description=data.description,
        image_url=data.image_url,
        destination_url=data.destination_url,
        button_text=data.button_text,
        redirect_seconds=data.redirect_seconds,
        is_active=data.is_active
    )
    
    db.add(new_redirect)
    db.commit()
    db.refresh(new_redirect)
    
    return new_redirect


def get_all_redirects(db: Session, page: int = 1, limit: int = 10):
    query = db.query(Redirect).order_by(Redirect.created_at.desc())
    
    return query.offset((page - 1) * limit).limit(limit).all()


def get_redirect_by_slug(db: Session, slug: str):
    return db.query(Redirect).filter(Redirect.slug == slug, Redirect.is_active == True).first()


def get_redirect_by_id(db: Session, redirect_id: int):
    return db.query(Redirect).filter(Redirect.id == redirect_id).first()


def increment_click_count(db: Session, redirect: Redirect):
    redirect.click_count += 1
    db.commit()
    db.refresh(redirect)
    return redirect


def update_redirect(db: Session, redirect_id: int, data: RedirectUpdate):
    redirect = db.query(Redirect).filter(Redirect.id == redirect_id).first()
    
    if not redirect:
        return None
    
    update_data = data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(redirect, field, value)
    
    db.commit()
    db.refresh(redirect)
    
    return redirect


def delete_redirect(db: Session, redirect_id: int):
    redirect = db.query(Redirect).filter(Redirect.id == redirect_id).first()
    
    if redirect:
        db.delete(redirect)
        db.commit()
        return True
    
    return False