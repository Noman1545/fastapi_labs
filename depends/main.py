from fastapi import FastAPI,Depends,Header,HTTPException
app=FastAPI()
def authorized_user(code:str=Header(None)):
    if code =="noman":
        return "authorized user"
    raise HTTPException(status_code=401,detail='unauthorized')
@app.get("/Secure-user")
def secure(token =Depends(authorized_user)):
    return {"welcome":"secured",
            'token':token}
    