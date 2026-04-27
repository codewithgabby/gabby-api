from sqlalchemy.orm import Session
from app.models.consultation import Consultation
from app.schemas.consultation import ConsultationCreate


def create_consultation(db: Session, data: ConsultationCreate):
    new_consultation = Consultation(
        name=data.name,
        email=data.email,
        service_type=data.service_type,
        message=data.message
    )

    db.add(new_consultation)
    db.commit()
    db.refresh(new_consultation)

    return new_consultation


def get_all_consultations(db: Session, status: str | None = None):
    query = db.query(Consultation)
    
    if status:
        query = query.filter(Consultation.status == status)
    
    return query.order_by(Consultation.id.desc()).all()


def update_status(db: Session, consultation_id: int, status: str):
    consultation = db.query(Consultation).filter(
        Consultation.id == consultation_id
    ).first()

    if consultation:
        consultation.status = status
        db.commit()
        db.refresh(consultation)

    return consultation

def hard_delete_consultation(db: Session, consultation_id: int):
    """Hard delete - permanently removes from database"""
    consultation = db.query(Consultation).filter(Consultation.id == consultation_id).first()
    
    if consultation:
        db.delete(consultation)
        db.commit()
        return True
    
    return False    