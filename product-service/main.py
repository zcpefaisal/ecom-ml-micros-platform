from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Product Service", desctiption="Product Service for ML Powerd E-commerce")

@app.get("/product-health")
def product_health():
    return {"status": "ok"}

class Product(BaseModel):
    id: int
    name: str
    price: float
    category: str


products_db = [
    {
        "id": 1,
        "name": "Laptop",
        "price": 999.99,
        "category": "Electronics"
    },
    {
        "id": 2,
        "name": "Book",
        "price": 19.99,
        "category": "Books"
    }
]


@app.get("/products", response_model=List[Product])
def get_products():
    return products_db


@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    for product in products_db:
        if product["id"] == product_id:
            return product
    return {"error": "Product Not Found"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)