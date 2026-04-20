from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

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