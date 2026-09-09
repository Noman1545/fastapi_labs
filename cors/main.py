from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app=FastAPI()

origin="http://localhost:5173"
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
    allow_origins=origin
)
@app.get("?")
def home():
    return{"message":"API created succesfully"}