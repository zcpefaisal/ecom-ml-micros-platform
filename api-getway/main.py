from fastapi import FastAPI, HTTPException
import httpx
import json

app = FastAPI(title="API Getway", description="API Getway for AI Powered E-commerce")

USER_SERVICE_URL = "http://localhost:8001"
PRODUCT_SERVICE_URL = "http://localhost:8002"
ORDER_SERVICE_URL = "http://localhost:8003"

@app.get("/")
def root():
    return {"status": "ok", "message": "Welcome to API getway"}

@app.get("/api-health")
def api_health():
    return {"status": "ok", "message": "API getway is up & running"}


# user get by Synchronous way
@app.get("/sync/users/{user_id}")
def get_sync_user(user_id: int):

    # ============================#
    # Note: with try, except      #
    # ============================#
    
    try:
        # Use synchronous Client
        with httpx.Client() as client:
            # Use synchronous client.get() method (no 'await')
            response = client.get(f"{USER_SERVICE_URL}/users/{user_id}")

            # Check for bad status codes (4xx or 5xx) from the downstream service
            # If 404 is returned, this line RAISES httpx.HTTPStatusError
            response.raise_for_status()

            # Use response.json() to extract the data payload
            return response.json()

    except httpx.RequestError as e:
        # Handle connection errors (e.g., service is down or DNS resolution failure)
        print(f"Error for connecting to User Service {e}")
        raise HTTPException(status_code=505, detail="User Service is currently unavailable")

    except httpx.HTTPStatusError as e:
        # This block catches 4xx errors (like 404, 403, etc.) and 5xx errors from the User Service
        print(f"User Service returned Error: {e}")
        raise HTTPException(status_code=e.response.status_code, detail=f"User Service Error: {e.response.status_code}")
        

    
# user get by asynchronous way
@app.get("/async/users/{user_id}")
async def get_async_user(user_id: int):

    # ============================#
    # Note: with try, except      #
    # ============================#

    try:
        # Use Asynchronous Client
        async with httpx.AsyncClient() as client:
            # Use Asynchronous client.get() method (yes 'await')
            response = await client.get(f"{USER_SERVICE_URL}/userss/{user_id}")

            # Check for bad status codes (4xx or 5xx) from the downstream service
            # If 404 is returned, this line RAISES httpx.HTTPStatusError
            response.raise_for_status()

            # Use response.json() to extract the data payload
            return response.json()
    except httpx.RequestError as e:
        # Handle connection errors (e.g., service is down or DNS resolution failure)
        print(f"Error for connection to User Service {e}")
        raise HTTPException(status_code=505, detail="User Service is currently unavailable")

    except httpx.HTTPStatusError as e:
        # This block catches 4xx errors (like 404, 403, etc.) and 5xx errors from the User Service
        print(f"User Service returned error: {e}")
        raise HTTPException(status_code=e.response.status_code, detail=f"User Service Error: {e.response.status_code}")



# products get by Synchronous way
@app.get("/sync/products")
def get_sync_products():

    # ============================#
    # Note: without try, except   #
    # ============================#
    
    # Use synchronous Client
    with httpx.Client() as client:
        # Use synchronous client.get() method (no 'await')
        response = client.get(f"{PRODUCT_SERVICE_URL}/products")

        # Use response.json() to extract the data payload
        return response.json()



# products get by Asynchronous way
@app.get("/asycn/products")
async def get_async_products():

    # ============================#
    # Note: without try, except   #
    # ============================#
    
    # Use synchronous Client
    async with httpx.AsyncClient() as client:
        # Use synchronous client.get() method (no 'await')
        response = await client.get(f"{PRODUCT_SERVICE_URL}/products")

        # Use response.json() to extract the data payload
        return response.json()



@app.post("/orders/")
async def create_order(order_data: dict):
    # Use synchronous Client
    async with httpx.AsyncClient() as client:
        # Use synchronous client.get() method (no 'await')
        response = await client.post(f"{ORDER_SERVICE_URL}/orders/", json=order_data)
        # Use response.json() to extract the data payload
        return response.json()

@app.get("/orders/{order_id}")
async def get_order(order_id: str):
    # Use synchronous Client
    async with httpx.AsyncClient() as client:
        # Use synchronous client.get() method (no 'await')
        response = await client.get(f"{ORDER_SERVICE_URL}/orders/{order_id}")
        # Use response.json() to extract the data payload
        return response.json()








if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)