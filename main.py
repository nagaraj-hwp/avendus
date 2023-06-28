from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

users = []

class User(BaseModel):
    id: int
    username: str
    email: str

@app.get("/users", response_model=List[User])
def get_users():
    return users

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    for user in users:
        if user.id == user_id:
            return user
    return {"error": "User not found"}

@app.post("/users", response_model=User)
def create_user(user: User):
    users.append(user)
    return user

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: User):
    for i, existing_user in enumerate(users):
        if existing_user.id == user_id:
            users[i] = user
            return user
    return {"error": "User not found"}

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for i, user in enumerate(users):
        if user.id == user_id:
            users.pop(i)
            return {"message": "User deleted successfully"}
    return {"error": "User not found"}
