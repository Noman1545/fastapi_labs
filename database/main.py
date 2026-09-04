from fastapi import Depends, FastAPI 
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
