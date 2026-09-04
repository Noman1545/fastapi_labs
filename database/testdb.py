from fastapi import Depends, FastAPI 
from sqlalchemy import create_engine,String,Integer,Column
from sqlalchemy.orm import sessionmaker,declarative_base,Session

app=FastAPI()

Database_url="sqlite:///./sample.db"
engine=create_engine(
    Database_url,
    connect_args={"check_same_thread":False}
)
SessionLocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)
Base=declarative_base()

class Student(Base):
    __tablename__= "student-data"

    ID =Column(Integer,primary_key=True,index=True)
    Name=Column(String)
    
Base.metadata.create_all(bind=engine)
def show_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.get("/home")
def home(db:Session=Depends(show_db)):
    return {'message':'database created'}
    