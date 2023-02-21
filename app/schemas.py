import datetime as _date
import app.database as _database
from datetime import date
import pydantic as _pydantic

from fastapi import File,UploadFile
from typing import Dict, FrozenSet, List, Optional, Sequence, Set, Tuple, Union
from sqlalchemy_utils import URLType


class BasePet(_pydantic.BaseModel):
    pet_type:str

    
class Pet(_pydantic.BaseModel): 
    
    pet_type:str
    pet_gender:str
    pet_size:str
    pet_age:str 
    # pet_photo:str
    pet_goodWithChildren:bool
    
    # have_owner:bool
      
    
class customer(_pydantic.BaseModel):
    customerId =int
 
    
class CreateCustomer(customer): 
    customer_name:str
    customer_phone:int
    gender:str
    petId:int
       
  
class Adoption(_pydantic.BaseModel):
    customerId:int
    petId:int
import datetime  



# class CreateAdoptionDateRequest(Adoption): 
#     # customer_name:str
#     # customer_phone:int
#     fromDate:datetime.date.today()
#     toDate:datetime.date.today()
           