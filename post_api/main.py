from fastapi.responses import JSONResponse

from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field,computed_field
from typing import Annotated, Literal
import json

app=FastAPI()

class patient(BaseModel):
    id:Annotated[str,Field(...,description="id of the patient",examples=['p001'])]
    name:Annotated[str,Field(...,description='name of the student')]
    city:Annotated[str,Field(...,description='add your city')]
    age:Annotated[int,Field(...,gt=0,lt=100,description='add patient age')]
    gender:Annotated[Literal['male','female'],Field(...,description='specify gender')]
    height:Annotated[float,Field(...,description='height in meters')]
    weight:Annotated[int,Field(...,description='add patient weight in kg')]
    
    @computed_field
    @property
    def bmi(self) -> float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 35:
            return 'Overweight'
        else:
             return "obese"
def show_data():
    with open ('patient.json','r') as f:
        data =json.load(f)
        return data
def save_data(data):
    with open ('patient.json','w') as f:
        json.dump(data,f)
    
@app.post("/post")
def create_patient(p:patient):
        data=show_data()
        if p.id in data:
            raise HTTPException(status_code=400,detail='id already exist')
        data[p.id]=p.model_dump(exclude=['id'])
        save_data(data)
        return JSONResponse(status_code=200,content={'message':'patient created'})
