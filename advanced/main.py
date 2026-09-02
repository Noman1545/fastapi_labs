from fastapi import FastAPI,status,HTTPException    
from pydantic import BaseModel
app = FastAPI()

@app.post("/todo",status_code=status.HTTP_201_CREATED)
def create_todo(todo:dict):
    return {
        'message': 'Todo item created successfully',
        'todo': todo
    }
    raise HTTPException(status_code=400, detail="Invalid todo item")