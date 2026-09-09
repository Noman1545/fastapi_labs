from fastapi import FastAPI,HTTPException,File,UploadFile
from fastapi import staticfiles
from fastapi.staticfiles import StaticFiles
import os 
import shutil

app =FastAPI()
UPLOADS="uploads"
if not os.path.exists(UPLOADS):
    os.makedirs(UPLOADS)
    
app.mount("/files",StaticFiles(directory=UPLOADS),name="files")
@app.post("/upload")
def upload_file(file:UploadFile=File(...)):
    filename=file.filename
    file_path=os.path.join(UPLOADS,filename)
    if not filename:
        raise HTTPException(status_code=404,detail="invalid")
    with open (file_path,"wb") as buffer:
        shutil.copyfileobj(file.file,buffer)
    return{"message":"file created",
           "filename":filename,
           "file url":f"http://127.0.0.1:8000/files/{filename}"}
        
@app.get("/file/{filename}")
def show_file(filename:str):
    file_path=os.path.join(UPLOADS,filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404,detail="missing")
    return f"http://127.0.0.1:8000/files/{filename}"
@app.get("/")
def home():
    return {"message":"file uploaded"}