from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate


def create_product(db: Session, data: ProductCreate):
    new_product = Product(
        name=data.name,
        description=data.description,
        link=data.link,
        type=data.type
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


def get_all_products(db: Session):
    return db.query(Product).filter(Product.is_active == True).all()


def delete_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if product:
        product.is_active = False  # Soft delete
        db.commit()
        db.refresh(product)
    
    return product