from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field    
from typing import Annotated

app = FastAPI()
todos=[]
class Address(BaseModel):
    street: Annotated[str, Field(..., description="The street of the address")]
    city: Annotated[str, Field(..., description="The city of the address")]
    state: Annotated[str, Field(..., description="The state of the address")]

class User(BaseModel):
    id: Annotated[int, Field(..., description="The ID of the todo item")] 
    title: str =Field(..., description="The title of the todo item")
    description: str = Field(..., description="The description of the todo item")
    completed: Annotated[bool, Field(..., description="The completion status of the todo item")]
    address: Annotated[Address, Field(..., description="The address of the todo item")]
    
@app.post("/todos/")
def create_todo(user: User):
    todos.append(user)
    return {
        'message': 'Todo item created successfully',
        'todo': user
    }
@app.get('/todos')
def get_todos():
    return todos

@app.get('/get_todo/{id}')
def get_todo(id:int):
    for todo in todos:
        if todo.id==id:
            return todo
    raise HTTPException(status_code=404, detail="Todo item not found")

@app.put('/edit/{id}')
def edit_user(id:int, user:User):
    for index, todo in enumerate(todos):
        if todo.id==id:
            todos[index]=user
            return {
                'message': 'Todo item updated successfully',
                'todo': user
            }
    raise HTTPException(status_code=404, detail="Todo item not found")