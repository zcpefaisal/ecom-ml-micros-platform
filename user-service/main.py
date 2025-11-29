from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str


users = []
user_id_counter = 1 # to generate unique user ids

@app.get("/user-health")
def user_health():
    return {"status": "OK"}

@app.post("/user-create")
async def user_create(user_create: UserCreate):
    global user_id_counter

    user_data = {
        "id": user_id_counter, # this will generate from DB auto increment
        "name": user_create.name,
        "email": user_create.email,
        "password": user_create.password # this should be hashed
    }
    users.append(user_data)
    user_id_counter += 1
    return user_data
    