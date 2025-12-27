from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from typing import List
import logging

from models import User, UserCreate, UserRead, UserUpdate
from database import engine, create_db_and_tables, get_session
from auth import hash_password, verify_password, create_access_token


# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="User Service", description="User Service for ML Powered E-commerce")


#CORS Middleware
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
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "user-service"}

# Create User
@app.post("/user-create", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def user_create(user_create: UserCreate, session: Session = Depends(get_session)):

    existing_user = session.exec(
        select(User).where(User.email == user_create.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already registered"
        )
    hashed_pwd = hash_password(user_create.password)
    db_user = User(
        email=user_create.email,
        full_name=user_create.full_name,
        hashed_password=hashed_pwd
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    logger.info(f"User created with email: {db_user.email}")
    return db_user

    
# Get user by ID
@app.get("/users/{user_id}", response_model=UserRead)
def user_get(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    return user

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
