from database import engine
from models import User
from auth import hash_password
from sqlmodel import Session, select
import logging

logger = logging.getLogger(__name__)

# Initialize default data
def init_data():
    """Initialize default data in the database."""
    try:
        with Session(engine) as session:
            # Create default admin user
            admin_exists = session.exec(select(User).where(User.email == "admin@example.com")).first()
            if not admin_exists:
                admin_user = User(
                    email="admin@example.com",
                    full_name="System Administrator",
                    hashed_password=hash_password("Admin@123"),
                    is_active=True
                )
                session.add(admin_user)
                logger.info("Admin user created successfully.")
            
            #create default customer user
            customer_exists = session.exec(select(User).where(User.email == "customer@example")).first()
            if not customer_exists:
                customer_user = User(
                    email="customer@example.com",
                    full_name="Default Customer",
                    hashed_password=hash_password("Customer@123"),
                    is_active=True
                )
                session.add(customer_user)
                logger.info("Customer user created successfully.")
            
            session.commit()
            logger.info("Initial data setup completed.")

    except Exception as e:
        logger.error(f"Error initialzing data setup: {e}")


