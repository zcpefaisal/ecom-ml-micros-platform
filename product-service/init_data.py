from database import engine
from models import Product
from sqlmodel import Session, select
import logging

logger = logging.getLogger(__name__)

# Initialize default data
def seed_products():
    """Initialize default data in the database."""
    try:
        with Session(engine) as session:
            # Create default products
            products = [
                {"name": "Laptop", "price": 999.99, "category": "Electronics", "stock_quantity": 50},
                {"name": "Smartphone", "price": 699.99, "category": "Electronics", "stock_quantity": 100},
                {"name": "Book", "price": 29.99, "category": "Books", "stock_quantity": 200},
                {"name": "T-shirt", "price": 19.99, "category": "Clothing", "stock_quantity": 150},
                {"name": "Wireless Headphones", "price": 149.50, "category": "Electronics", "stock_quantity": 75},
                {"name": "Coffee Maker", "price": 89.99, "category": "Home Appliances", "stock_quantity": 30},
                {"name": "Yoga Mat", "price": 25.00, "category": "Fitness", "stock_quantity": 120},
                {"name": "Desk Lamp", "price": 35.99, "category": "Furniture", "stock_quantity": 45},
                {"name": "Running Shoes", "price": 110.00, "category": "Footwear", "stock_quantity": 60},
                {"name": "Gaming Mouse", "price": 54.99, "category": "Electronics", "stock_quantity": 85},
                {"name": "Ceramic Mug", "price": 12.50, "category": "Kitchen", "stock_quantity": 300},
                {"name": "Backpack", "price": 45.00, "category": "Accessories", "stock_quantity": 90},
                {"name": "Water Bottle", "price": 15.99, "category": "Fitness", "stock_quantity": 250},
                {"name": "Electric Kettle", "price": 40.00, "category": "Home Appliances", "stock_quantity": 40},
                {"name": "Bluetooth Speaker", "price": 59.99, "category": "Electronics", "stock_quantity": 110},
                {"name": "Leather Wallet", "price": 35.00, "category": "Accessories", "stock_quantity": 70},
                {"name": "Notebook", "price": 8.99, "category": "Stationery", "stock_quantity": 500},
                {"name": "Desk Chair", "price": 199.99, "category": "Furniture", "stock_quantity": 15},
                {"name": "Sunglasses", "price": 120.00, "category": "Accessories", "stock_quantity": 55},
                {"name": "Winter Jacket", "price": 145.00, "category": "Clothing", "stock_quantity": 25}
            ]

            for product in products:
                product_exists = session.exec(select(Product).where(Product.name == product["name"])).first()
                if not product_exists:
                    new_product = Product(
                        name=product["name"],
                        price=product["price"],
                        category=product["category"],
                        stock_quantity=product["stock_quantity"]
                    )
                    session.add(new_product)
                    logger.info(f"Product '{product['name']}' created successfully.")

            session.commit()
            logger.info("Initial product data setup completed.")
            
    except Exception as e:
        logger.error(f"Error initializing product data setup: {e}")