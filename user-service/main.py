from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from typing import List
import logging

from models import User, UserCreate, UserRead, UserUpdate
from database import engine, create_db_and_tables, get_session
from auth import hash_password, verify_password, create_access_token
from init_data import init_data 


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
    init_data() # Initialize default data
    logger.info("Database tables created")


# Health Check
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "user-service"}


# Login user
@app.post("/login")
def login(email: str, password: str, session: Session = Depends(get_session)):

    # Find user by email
    user = session.exec(
        select(User).where(User.email == email)
    ).first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create JWT token
    access_token = create_access_token(data={"sub": user.email})

    return {
        "access_token": access_token, 
        "token_type": "bearer", 
        "user": UserRead.from_orm(user)
    }


# Create User
@app.post("/user-create", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user_create: UserCreate, session: Session = Depends(get_session)):

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
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    return user

# Get all users
@app.get("/users", response_model=List[UserRead])
def get_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users


# Update user
@app.patch("/users/{user_id}", response_model=UserRead)
def update_user(user_id: int, user_update: UserUpdate, session: Session = Depends(get_session)):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    user_update = user_update.dict(exclude_unset=True)
    if "password" in user_update:
        user_update["hashed_password"] = hash_password(user_update.pop("password"))

    for key, value in user_update.items():
        setattr(db_user, key, value)

    db_user.update_at = datetime.utcnow()
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user 
    

# Delete user
app.delete("/users/{user_id}")
def user_delete(user_id: int, session: Session = Depends(get_session)):
    user_delete = session.exec(select(User).where(User.id == user_id)).first()
    if not user_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    session.delete(user_delete)
    session.commit()

    return {"detail": "User deleted successfully"}









if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
