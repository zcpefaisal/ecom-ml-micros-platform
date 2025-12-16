from datetime import datetime
from mimetypes import init
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Order Service", description="Order Service for ML Powerd E-commerce")


@app.get("/order-health")
def order_health():
    return {"status": "OK"}


class OrderItem(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderCreate(BaseModel):
    user_id: int
    items: List[OrderItem]
    shipping_address: str

class OrderResponse(BaseModel):
    order_id: str
    user_id: int
    items: List[OrderItem]
    total_amount: float
    status: str
    created_at: datetime

# Order store in-memory
orders_db = {}

@app.post("/orders/", response_model=OrderResponse)
def order_create(order_data: OrderCreate):
    order_id = str(uuid.uuid4())

    # Calculate item total price
    total_amount = sum(item.price * item.quantity for item in order_data.items)

    order = {
        "order_id": order_id,
        "user_id": order_data.user_id,
        "items": [item.dict() for item in order_data.items],
        "total_amount": total_amount,
        "status": "pending",
        "created_at": datetime.utcnow()
    }

    orders_db[order_id] = order
    return order


@app.get("/orders/{order_id}")
def get_order(order_id: str):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found for this order id")
    return orders_db[order_id]


@app.get("/users/{user_id}/orders")
def get_user_orders(user_id: int):
    user_orders = [order for order in orders_db.values() if order["user_id"] == user_id]
    if not user_orders:
        raise HTTPException(status_code=404, detail="Order not found for this user")
    return user_orders




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8003)