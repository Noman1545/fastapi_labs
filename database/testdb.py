from fastapi import FastAPI,Depends
from sqlalchemy import create_engine,Column ,Integer,String,Boolean
from sqlalchemy.orm import sessionmaker,declarative_base,Session

app=FastAPI()
Database_url="sqlite:///./test.db"
engine=create_engine(
    Database_url,connect_args={"check_same_thread":False}
)
SessionLocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)
Base=declarative_base()

class Todo(Base):
    __tablename__='todos'
    
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String)
    completed=Column(Boolean,default=False)
    
Base.metadata.create_all(bind=engine)
def get_db():
    db=SessionLocal()
    try :
        yield db
    finally:
        db.close()
@app.get("/")
def home(db :Session= Depends(get_db)):
    return {'message':'db created successfully'}