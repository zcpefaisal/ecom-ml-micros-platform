from shared.circuit_breaker import CircuitBreaker
import os

class ServieClient:
    def __init__(self):
        self.circuit_breaker = CircuitBreaker()
        self.user_service_url = os.getenv("USER_SERVICE_URL", "http://user-service:8001")
        self.product_service_url = os.getenv("PRODUCT_SERVICE_URL", "http://product-service:8002")

        async def get_user(self, user_id: int):
            """Get user with circuit breaker protection"""
            url = f"{self.user_service_url}/users/{user_id}"
            
            fallback_user = {
                "id": user_id,
                "full_name": "Unknown User",
                "email": "customer@example.com,
            }
            return await self.circuit_breaker.call_with_fallback(
                method="GET",
                url=url,
                fallback_value=fallback_user
            )
        

        async def get_product(self, product_id: int):
            """Get product with circuit breaker protection"""
            url = f"{self.product_service_url}/products/{product_id}"
            
            fallback_product = {
                "id": product_id,
                "name": "Laptop",
                "price": 0.0,
            }
            return await self.circuit_breaker.call_with_fallback(
                method="GET",
                url=url,
                fallback_value=fallback_product
            )