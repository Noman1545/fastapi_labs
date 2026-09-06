from fastapi import Depends, FastAPI ,HTTPException
from sqlalchemy import create_engine,String,Integer,Column
from sqlalchemy.orm import sessionmaker,declarative_base,Session

app=FastAPI()

Database_url="sqlite:///./new-sample.db"

engine =create_engine(Database_url,connect_args={"check_same_thread":False})
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()

class Student(Base):
    __tablename__='student-data'
    ID=Column(Integer,primary_key=True,index=True)
    Name=Column(String)
    Age=Column(Integer)
Base.metadata.create_all(bind=engine)
def show():
        db=SessionLocal()
        try:
            yield db
        finally:
            db.close()
@app.post("/")
def insert_data(Name:str,Age:int,db:Session=Depends(show)):
    s1=Student(Name=Name,Age=Age)
    db.add(s1)
    db.commit()
    db.refresh(s1)
    return {"message":s1}
@app.get("/show")
def get_data(db:Session=Depends(show)):
    data=db.query(Student).all()
    return{
        'length':len(data),
        'data':data
    }
@app.get("/show/{student_id}")
def data_by_id(student_id:int,db:Session=Depends(show)):
    data_id=db.query(Student).filter(Student.ID==student_id).first()
    if not data_id:
        raise HTTPException(status_code=404,detail="ID not found")
    return{
        "student ID":data_id
    }

@app.put("/edit/{student_id}")
def update_data(student_id:int,Name:str,Age:int,db:Session=Depends(show)):
    update=db.query(Student).filter(Student.ID==student_id).first()
    if not update:
        raise HTTPException(status_code=404,detail="ID not found")
    update.Name=Name
    update.Age=Age
    db.commit()
    db.refresh(update)
    return update
@app.delete("/delete/{student_id}")
def delete_data(student_id:int,db:Session=Depends(show)):
    delete_id=db.query(Student).filter(Student.ID==student_id).first()
    if not delete_data:
        raise HTTPException(status_code=404,detail="ID not found")
 
    db.delete(delete_id)
    db.commit()
    return {"message":"deleted"}