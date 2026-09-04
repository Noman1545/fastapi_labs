from fastapi import FastAPI,Request
import time
app=FastAPI()

@app.middleware("http")
async def log_process_time(request:Request,call_next):
    start_time=time.time()
    response= await call_next(request)
    execution_time=time.time()-start_time
    response.headers["Execution_Time"]=f"{execution_time} sec"
    return response

@app.get("/")
def home():
    return{'message':'execution completed'}