from sqlmodel import create_engine, SQLModel, Session
import os

# Get database URL from environment variable or use default
DATABASE_URL = os.getenv("DATABASE_URL", 'postgresql://postgres:password@localhost:5432/userdb')

# Create engine
engine = create_engine(DATABASE_URL, echo=True) # echo=True for showing SQL queries

def create_db_and_tables():
    # Create all tables on startup
    SQLModel.metadata.create_all(engine)


def get_session():
    # Dependency for FastAPI to get database session
    with Session(engine) as session:
        yield session
