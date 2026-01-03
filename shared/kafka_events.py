from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class EventType(str, Enum):
    USER_CREATED = "user.created"
    USER_UPDATED = "user.updated"
    ORDER_CREATED = "order.created"
    ORDER_UPDATED = "order.updated"
    ORDER_CANCELLED = "order.cancelled"
    PRODUCT_CREATED = "product.created"
    PRODUCT_UPDATED = "product.updated"
    PRODUCT_STOCK_UPDATED = "product.stock.updated"

class BaseEvent(BaseModel):
    event_id: str
    event_type: EventType
    timestamp: datetime
    producer: str
    data: dict

class UserCreatedEvent(BaseEvent):
    event_type: EventType = EventType.USER_CREATED
    data: dict  # Should contain user details

class OrderCreatedEvent(BaseEvent):
    event_type: EventType = EventType.ORDER_CREATED
    data: dict  # Should contain order details

