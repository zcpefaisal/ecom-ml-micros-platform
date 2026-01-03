from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from typing import List, Optional
import logging
import os

from models import Product, ProductBase, ProductCreate, ProductRead, ProductUpdate
from database import get_session, engine, create_db_and_tables

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Product Service", desctiption="Product Service for ML Powerd E-commerce")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event to create database tables
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    
    # Only seed data in development or testing environments
    if os.getenv("ENVIRONMENT") in ["development", "testing"] and \
        os.getenv("SEED_DATABASE", "true").lower() == "true":
        
        from init_data import seed_products
        seed_products() # Initialize default data
        logger.info("Database Seeded with initial data")
    else:
        logger.info("Skipping database seeding")


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "product-service"}

# Create product
@app.post("/products/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, session: Session = Depends(get_session)):
    db_product = Product.from_orm(product)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


# Get products with optional filters
@app.get("/products", response_model=List[ProductRead])
def get_products(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    session: Session = Depends(get_session)
):

    query = select(Product)
    if category:
        query = query.where(Product.category == category)
    if min_price is not None:
        query = query.where(Product.price >= min_price)
    if max_price is not None:
        query = query.where(Product.price <= max_price)

    query = query.offset(skip).limit(limit)
    products = session.exec(query).all()

    return products


# Get product by ID
@app.get("/products/{product_id}", response_model=ProductRead)
def get_product(product_id: int, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(
            status_code=404, 
            detail="Product Not Found"
        )
    return product

# Update product by ID
@app.patch("/products/{product_id}", response_model=ProductRead)
def update_product(product_id: int, product_update: ProductUpdate, session: Session = Depends(get_session)):
    db_product = session.get(Product, product_id)
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product Not Found"
        )
    product_data = product_update.dict(exclude_unset=True)
    for key, value in product_data.items():
        setattr(db_product, key, value)

    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


# Delete product by ID
@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Product Not Found"
        )
    session.delete(product)
    session.commit()
    return {"detail": "Product deleted successfully"}





if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)