from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description= 'Patient id', examples=['P001'])]
    name: Annotated[str, Field(..., description= 'Name of the patient')]
    city: Annotated[str, Field(..., description= 'City of patient')]
    age: Annotated[int, Field(..., gt=0, description= 'Age of patient')]
    gender: Annotated[Literal['Male', 'female', 'others'], Field(..., description= 'Gender of patient')]
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


# Model for updating patient data
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    city: Annotated[Optional[str], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


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
def view_patient(patient_id: str = Path(..., description = 'id of patient' , examples= 'P001') ):
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


# Put method
@app.put('/edit/{patient_id}')
def update_patient(patient_id:str, patient_update: PatientUpdate):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')

    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key]= value

    # existing_patient_info -> pydantic object -> updated bmi + verdict
    existing_patient_info['id'] = patient_id
    patient_pydantic_obj = Patient(**existing_patient_info)

    # pydantic object -> dict
    existing_patient_info = patient_pydantic_obj.model_dump(exclude= 'id')

    # add this dict to data
    data[patient_id] = existing_patient_info

    # save data
    save_data(data)

    return JSONResponse(status_code= 202, content={'message': 'patient updated successfully'})

# Delete method
@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):

    # laod data
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail= 'patient not found')

    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code= 200, content={'message': 'patient deleted'})
