from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import json

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description= 'Patient id', examples=['P001'])]
    name: Annotated[str, Field(..., description= 'Name of the patient')]
    city: Annotated[str, Field(..., description= 'City of patient')]
    age: Annotated[int, Field(..., gt=0, description= 'Age of patient')]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description= 'Gender of patient')]
    height: Annotated[float, Field(..., description= 'Height of patient in mtrs')]
    weight: Annotated[float, Field(..., description= 'Weight of patient in kgs')]

@computed_field
@property
def bmi(self) -> float:
    bmi = round(self.weight/(self.height**2), 2)
    return bmi

@computed_field
@property
def verdict(self) -> str:
    if self.bmi < 18:
        return 'Underweight'
    elif self.bmi < 25:
        return 'Normal'
    elif self.bmi < 30:
        return 'Normal'
    else:
        return 'Obese'


def load_data():
    with open('patient.json', 'r') as f:
        data = json.load(f)

    return data

# function for save new patient data into json file 
def save_data(data):
    with open('patient.json', 'w') as f:
        json.dump(data, f)


#......Get Endpoints......
@app.get("/")
def hello():
    return{
        "message": "patient Management System"
    }


@app.get("/about")
def about():
    return{
        'message': 'A fully functional api to manage your patient record.'
    }


@app.get('/view')
def view():
    data = load_data()

    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description = 'id of patient' , example= 'P001') ):
    # load patient data
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code= 404, detail= 'patient not found')


@app.get('/sort')
def sort_patients(sort_by: str = Query (..., description = 'sort on the basis or height, weight'), order : str = Query ('asc' , description = 'sort in asc and desc order')):

    valid_fields = ['height', 'weight']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail = 'Invalid field select from {valid_fields}')

    if order not in ['asc' , 'desc']:
        raise HTTPException(status_code=400, detail = 'Invalid code select between ascending and descending')

    data = load_data()

    sort_order = True if order == 'desc'else False
    sorted_data = sorted(data.values(), key = lambda x: x.get(sort_by, 0), reverse= sort_order)
    
    return sorted_data


#......Post Endpoints......
@app.post('/create')
def create_patient(patient: Patient):

    #load existing data
    data = load_data()

    # check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code= 400, detail= 'patient already exist')

    # add new patient to database
    data[patient.id] = patient.model_dump(exclude=['id'])

    # save into the json file
    save_data(data)
    
    return JSONResponse(status_code=201, content= {'message': 'Patient created successfully'})