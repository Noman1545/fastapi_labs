from jose import jwt,JWTError
from fastapi import FastAPI,HTTPException,Header,Depends
from datetime import datetime,timedelta,timezone
import os
from dotenv import load_dotenv
app=FastAPI()

SecretKey='noman1125'
Algorithm="HS512"

def create_token(data:dict):
    to_encode=data.copy()
    expiry=datetime.now(timezone.utc) + timedelta( minutes=30)
    to_encode.update({"exp":expiry})
    token=jwt.encode(to_encode,SecretKey,algorithm=Algorithm)
    return token

def verify_token(token:str=Header(None)):
    if token is None:
        raise HTTPException(status_code=401,detail="token is missing")
    try:
        payload=jwt.decode(token,SecretKey,algorithms=[Algorithm])
        return payload
    except JWTError:
        raise HTTPException(status_code=404,detail="invalid token")
    
@app.post("/")
def login(username:str,password:str):
    if username !='noman' or password !="noman1125":
        raise HTTPException(status_code=404,detail="invalid")
    token =create_token({"sub":username})
    return {"access":token}
@app.get("/")
def authorized_user(token:dict=Depends(verify_token)):
    return {"message":"verified user"}
    
    