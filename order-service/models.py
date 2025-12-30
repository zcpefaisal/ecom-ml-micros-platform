from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELED = "canceled"

# Base model for OrderItem (creating/reading)
class OrderItemBase(SQLModel):
    prodict_id: int = Field(foreign_key="product.id")
    quantity: int = Field(gt=0)
    price: float = Field(gt=0)

# OrderItem model representing the order_items table
class OrderItem(OrderItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: Optional[int] = Field(default=None, foreign_key="order.id")
    order: Optional["Order"] = Relationship(back_populates="items")

# Base model for Order (creating/reading)
class OrderBase(SQLModel):
    user_id: int
    status: OrderStatus = OrderStatus.PENDING
    shipping_address: str

# Order model representing the orders table
class Order(OrderBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    total_amount: float = Field(default=0.0, ge=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    items: List[OrderItem] = Relationship(
        back_populates="order",
        sa_ralationship_kwargs={"cascade": "all, delete-orphan"}
    )

# Pydantic models for API request
class OrderCreate(SQLModel):
    user_id: int
    items: List[OrderItemBase]
    shipping_address: str

# Pydantic models for API response
class OrderRead(SQLModel):
    id: int
    created_at: datetime
    items: List[OrderItemBase]