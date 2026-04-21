from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.product import Product

from app.schemas.product import ProductCreate, ProductResponse
from app.services.product_service import create_product, get_all_products, delete_product
from app.dependencies import verify_admin, get_db

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductResponse)
def create_product_endpoint(
    data: ProductCreate, 
    db: Session = Depends(get_db),
    _: str = Depends(verify_admin)
):
    return create_product(db, data)


@router.get("/", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return get_all_products(db)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Public: Get a single product by ID"""
    product = db.query(Product).filter(Product.id == product_id, Product.is_active == True).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product_endpoint(
    product_id: int,
    data: ProductCreate,
    db: Session = Depends(get_db),
    _: str = Depends(verify_admin)
):
    """Admin: Update a product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product.name = data.name
    product.description = data.description
    product.link = data.link
    product.type = data.type
    if data.image_url:
        product.image_url = str(data.image_url)
    
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}")
def delete_product_endpoint(
    product_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(verify_admin)
):
    product = delete_product(db, product_id)
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {"message": f"Product '{product.name}' deleted successfully"}