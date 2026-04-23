from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.models.product import Product

from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
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
def get_products(
    search: str | None = Query(None, description="Search in name and description"),
    type: str | None = Query(None, description="Filter by type: saas, tool, app, physical"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(9, ge=1, le=50, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Public: Get products with pagination, search, and filtering"""
    query = db.query(Product).filter(Product.is_active == True)
    
    if type:
        query = query.filter(Product.type == type)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            Product.name.ilike(search_term) | 
            Product.description.ilike(search_term)
        )
    
    products = query.order_by(Product.created_at.desc())\
        .offset((page - 1) * limit)\
        .limit(limit)\
        .all()
    
    return products


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
    data: ProductUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(verify_admin)
):
    """Admin: Update a product (partial updates allowed)"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Only update fields that were sent
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
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