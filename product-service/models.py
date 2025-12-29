from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class ProductBase(SQLModel):
    name: str = Field(index=True)
    description: Optional[str] = None
    price: float = Field(gt=0)
    category: str = Field(index=True)
    stock_quantity: int = Field(default=0, ge=0)
    is_active: bool = Field(default=True)

class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int
    created_at: datetime

class ProductUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    stock_quantity: Optional[int] = None
    is_active: Optional[bool] = None