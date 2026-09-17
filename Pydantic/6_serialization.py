from pydantic import BaseModel

class Address(BaseModel):
    city: str
    town: str
    pin: str

class Patient(BaseModel):
    name: str
    age : int
    address : Address

address_dict = {'city': 'Bahawalpur', 'town': 'Model A', 'pin': '24862'}
address1 = Address(**address_dict)

patient_dict = {'name': 'Talha', 'age': 20, 'address': address1}
patient1 = Patient(**patient_dict)

#......For Exporting Model......

# temp = patient1.model_dump()
# temp = patient1.model_dump_json()
temp = patient1.model_dump(exclude= {'address': ['pin']})

print(temp)
# print(patient1)