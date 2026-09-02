from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()
class User(BaseModel):
    id: int
    name: str
    password: str
class UserResponse(BaseModel):
    id: int
    name: str
@app.get("/users/", response_model=UserResponse)
def get_users():
    return {"id": 1, "name": "John Doe", "password": "secret"}