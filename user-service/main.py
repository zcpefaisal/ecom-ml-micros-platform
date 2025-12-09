from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

app = FastAPI(title="User Service", description="User Service for ML Powered E-commerce")


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

@app.post("/user-create", response_model=UserResponse)
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
    

@app.get("/users/{user_id}", response_model=UserResponse)

async def user_get(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
