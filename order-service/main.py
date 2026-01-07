from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from typing import List
import logging 

from models import Order, OrderItem, OrderCreate, OrderRead, OrderStatus
from database import create_db_and_tables, get_session
from service_client import ServieClient

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Order Service", description="Order Service for ML Powerd E-commerce")

# Initialize service client
service_client = ServieClient()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Startup event
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    logger.info("Database tables created")

# Health Check
@app.get("/health")
def health_check():
    return {"status": "ok", "service": "order-service"}

# Create a new order
@app.post("/orders/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def create_order(order_data: OrderCreate, session: Session = Depends(get_session)):

    # Validate user existence using circuit breaker protected call
    user = await service_client.get_user(order_data.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    
    # Validate products existence and get their details
    for item in order_data.items:
        product = await service_client.get_product(item.prodict_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Product with ID {item.prodict_id} not found"
            )
        

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

    # Create OrderItem instances
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

# Get order by ID
@app.get("/orders/{order_id}", response_model=OrderRead)
def get_order(order_id: int, session: Session = Depends(get_session)):
    db_order = session.get(Order, order_id)
    if not db_order:
        raise HTTPException(
            status_code=404, 
            detail="Order not found"
        )
    return db_order

# Get orders for a specific user
@app.get("/users/{user_id}/orders", response_model=List[OrderRead])
def get_user_orders(user_id: int, session: Session = Depends(get_session)):
    statements = select(Order).where(Order.user_id == user_id)
    db_orders = session.exec(statements).all()
    if not db_orders:
        raise HTTPException(
            status_code=404, 
            detail="Order not found for this user"
        )
    return db_orders

# Update order status
@app.patch("/orders/{order_id}/status", response_model=OrderRead)
def update_order_status(order_id: int, status: OrderStatus, session: Session = Depends(get_session)):
    db_order = session.get(Order, order_id)
    if not db_order:
        raise HTTPException(
            status_code=404, 
            detail="Order not found"
        )
    db_order.status = status
    session.add(db_order)
    session.commit()
    session.refresh(db_order)

    logger.info(f"Order ID: {db_order.id} status updated to {db_order.status}")
    return db_order


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8003)