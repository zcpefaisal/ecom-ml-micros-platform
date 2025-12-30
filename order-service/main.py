from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from typing import List
import logging 

from models import Order, OrderItem, OrderCreate, OrderRead, OrderStatus
from database import create_db_and_tables, get_session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Order Service", description="Order Service for ML Powerd E-commerce")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    logger.info("Database tables created")


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "order-service"}


@app.post("/orders/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(order_data: OrderCreate, session: Session = Depends(get_session)):

    # Calculate item total price
    total_amount = sum(item.price * item.quantity for item in order_data.items)
    
    # Create Order instance
    db_order = Order(
        user_id=order_data.user_id,
        shipping_address=order_data.shipping_address,
        total_amount=total_amount,
        status=OrderStatus.PENDING
    )

    session.add(db_order)
    session.commit()
    session.refresh(db_order)

    #Create OrderItem instances
    for item in order_data.items:
        db_item = OrderItem(
            order_id=db_order.id,
            prodict_id=item.prodict_id,
            quantity=item.quantity,
            price=item.price
        )
        session.add(db_item)
    session.commit()
    session.refresh(db_order)
    
    logger.info(f"Order created with ID: {db_order.id} for User ID: {db_order.user_id}")

    return db_order


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