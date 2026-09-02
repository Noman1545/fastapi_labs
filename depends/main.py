from fastapi import FastAPI,Depends
app=FastAPI()

def User():
    return "welcome"
@app.get("/home")
def user_get(user= Depends(User)):
    return user
@app.get("/about")
def about_user(user=Depends(User)):
    return user
