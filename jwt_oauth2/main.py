from fastapi import FastAPI,HTTPException,Depends
from jose import jwt,JWTError
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from datetime import datetime,timedelta,timezone
from passlib.context import CryptContext
app=FastAPI()
SECRETKEY='noman1125'
ALGORITHM='HS256'
ACCESS_TOKEN_EXPIRY=30
# password hashing adding extra strings
pwd_context=CryptContext(schemes=["bycrypt"],deprecated="auto")
# oauth setup
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")
fake_user_db={
    "admin":{
        "username":"admin",
        "hashed_password":pwd_context.hash("1125")
    }
}
def hash_pwd(password:str):
    return pwd_context.hash(password)
def verify_pwd(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)
def create_token(data:dict):
    to_encode=data.copy()
    exp=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRY)
    to_encode.update({"exp":exp})
    token=jwt.encode(to_encode,SECRETKEY,algorithm=ALGORITHM)
    return token

@app.post("/login")
def login(form_data:OAuth2PasswordRequestForm=Depends()):
    user=fake_user_db.get(form_data.username)
    if not user or not verify_pwd(form_data.password,user["hashed_password"]):
        raise HTTPException(status_code=400,detail="invalid username or password")
    access_token=create_token({"sub":form_data.username})
    return {"access_token":access_token,"token_type":"bearer"}
def verify_token(token:str=Depends(oauth2_scheme)):
    try:
        payload=jwt.decode(token,SECRETKEY,algorithms=[ALGORITHM])
        username=payload.get("sub")
    
        if username is None:
            raise HTTPException(status_code=401,detail="invalid token")
        return username
    except jwt.JWTError:
        raise HTTPException(status_code=401,detail="invalid")

@app.get("/protected")
def protected_route(username:str=Depends(verify_token)):
    return username
    
        