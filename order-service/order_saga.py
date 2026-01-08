import uuid
from saga_orchestrator import SagaOrchestrator, SagaStep
from service_client import ServiceClient
from models import Order, OrderItem
from database import get_session
from sqlmodel import Session

class OrderSaga:
    def __init__(self, order_data: dict, session: Session):
        self.order_data = order_data
        self.session = session
        self.saga_id = str(uuid.uuid4())
        self.service_client = ServiceClient()
        
    async def create_order_saga(self):
        """Create order using saga pattern"""
        saga = SagaOrchestrator(self.saga_id)
        
        # Reserve products (check stock)
        async def reserve_products():
            for item in self.order_data["items"]:
                # Call product service to reserve stock
                await self.service_client.reserve_product(
                    product_id=item["product_id"],
                    quantity=item["quantity"]
                )
                
        async def compensate_reserve_products():
            # Release reserved stock
            for item in self.order_data["items"]:
                await self.service_client.release_product(
                    product_id=item["product_id"],
                    quantity=item["quantity"]
                )
        
        saga.add_step(SagaStep(
            name="reserve_products",
            execute=reserve_products,
            compensate=compensate_reserve_products
        ))
        
        # Create order in database
        async def create_order_db():
            order = Order(
                user_id=self.order_data["user_id"],
                shipping_address=self.order_data["shipping_address"]
            )
            self.session.add(order)
            self.session.commit()
            self.session.refresh(order)
            self.order_id = order.id
            
        async def compensate_create_order_db():
            # Delete order if created
            if hasattr(self, 'order_id'):
                order = self.session.get(Order, self.order_id)
                if order:
                    self.session.delete(order)
                    self.session.commit()
                    
        saga.add_step(SagaStep(
            name="create_order_db",
            execute=create_order_db,
            compensate=compensate_create_order_db
        ))
        
        # Create payment (simulated)
        async def create_payment():
            # Call payment service
            payment_data = {
                "order_id": self.order_id,
                "amount": self.order_data["total_amount"],
                "user_id": self.order_data["user_id"]
            }
            await self.service_client.create_payment(payment_data)
            
        async def compensate_create_payment():
            # Cancel payment
            await self.service_client.cancel_payment(self.order_id)
            
        saga.add_step(SagaStep(
            name="create_payment",
            execute=create_payment,
            compensate=compensate_create_payment
        ))
        
        # Execute saga
        success = await saga.execute()
        return success, self.order_id if success else None