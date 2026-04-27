from sqlalchemy.orm import Session
from app.models.contact import Contact
from app.schemas.contact import ContactCreate


def create_contact(db: Session, contact: ContactCreate):
    new_contact = Contact(
        name=contact.name,
        email=contact.email,
        message=contact.message
    )

    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)

    return new_contact


def get_all_contacts(db: Session):
    return db.query(Contact).order_by(Contact.created_at.desc()).all()


def hard_delete_contact(db: Session, contact_id: int):
    """Hard delete - permanently removes from database"""
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    
    if contact:
        db.delete(contact)
        db.commit()
        return True
    
    return False





   

  