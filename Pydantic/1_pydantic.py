from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator, computed_field
from typing import List , Dict , Optional, Annotated

class Patient(BaseModel):

    name: Annotated[str, Field(max_length=50, title= 'Name of patient', description= 'Give the name of patient less than 50 chars', examples = ['Talha'])]
    email: EmailStr
    linkedin: AnyUrl
    age: int = Field(gt = 10, lt = 100)
    height: float
    weight: float
    married: Annotated[bool, Field(default= None, description= 'Is the patient married or not')]
    allergies: Optional[list[str]] = None
    contact_detail: Dict[str, str]
    address: Adress

# ......Learn Field validator, Transform value......
    @field_validator('email')
    @classmethod
    def email_validator(cls , value):

        valid_domains = ['ubl.com', 'iub.edu.pk']
        domain_name = value.split('@')[-1]

        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')

        return value

    @field_validator('name')
    @classmethod
    def transform_name(cls, value):

        return value.upper()

# ......Field Validator Mode......
    @field_validator('age' , mode= 'before')
    @classmethod
    def age_validation(cls, value):
        if 0 < value < 100:
            return value
        else:
            raise ValueError('Age should be in between 0 and 100')

# ......Model Validator......
    @model_validator(mode= 'after')
    def validate_emergency_contact(self):
        if self.age > 50 and 'emergency' not in self.contact_detail:
            raise ValueError('Age greater than 50 must have emergency contact in contact_detail')
        else:
            return self

#......Computed Field......
    @computed_field
    @property
    def calculate_bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi

# ......Nested Model......
class Adress(BaseModel):
    city: str
    street: str
    pin: str

address_dict = {'city': 'Bahawalpur', 'street': 'street no 1', 'pin': '98734'}
address1 = Adress(**address_dict)


# ......Patient INFO......
patient_info = {'name': 'talha', 'email': 'mtalhaimran104@ubl.com', 'linkedin': 'https://www.linkedin.com/in/talha-imran-ai/', 'age': 60, 'height': 55.3, 'weight': 67.5, 'married': True, 'contact_detail': { 'phone': '1233', 'landline': '124321', 'emergency': '0000000'}, 'address': address1}

patient1 = Patient(**patient_info)


# ......insert patient data......
def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print('inserted')

# ......Update patient Data......
def update_patient_data(patient: Patient):
    print('Name =', patient.name)
    print('Mail =', patient.email)
    print('Lindedin =',patient.linkedin)
    print('Age =', patient.age)
    print('Height =', patient.height)
    print('Weight =', patient.weight)
    print('BMI =', patient.calculate_bmi)
    print('Married =', patient.married)
    print('Allergies =', patient.allergies)
    print('Contact_details =', patient.contact_detail)
    print('Address_pin =', patient.address.pin)
    print('Data Updated')


update_patient_data(patient1)
# insert_patient_data(patient1)
# print(patient1)
