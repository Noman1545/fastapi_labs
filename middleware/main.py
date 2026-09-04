from fastapi import FastAPI,Request
import time
app=FastAPI()

@app.middleware("http")
async def log_process_time(request:Request,call_next):
    start_time=time.time()
    response= await call_next(request)
    process_time=time.time()-start_time
    print(f"path: {request.url.path} process time is {process_time}")
    return response