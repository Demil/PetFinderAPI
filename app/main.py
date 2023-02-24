from typing import TYPE_CHECKING,Union
import fastapi as _fastapi
import app.schemas as _schemas
import app.services as _services
import sqlalchemy.orm as _orm
import app.models as _models
import app.database as _database
import sqlalchemy as _sql
import pydantic as _pydantic
import app.PetFinderAPI as _remote_api
from fastapi_pagination import LimitOffsetPage, paginate, add_pagination
from fastapi import File,UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import datetime as _date
import shutil



# create tables for database 
_services.manage_table()

def get_session():
    session=_database.SessionLocal()
    try:
        yield session
    finally:
        session.close()
 


app=_fastapi.FastAPI()
add_pagination(app)

#this is for adoprion button request
app.mount("/static",StaticFiles(directory="static"), name="static")
@app.get("/home/{search_item}", response_class=_fastapi.responses.HTMLResponse)
async def hello(request:_fastapi.Request, search_item:str):
    
    templates = _fastapi.templating.Jinja2Templates(directory="templates")
    return templates.TemplateResponse("petFinder.html", {"request": request, "name":search_item})


# This endpoint will create a new pet
# and store them in the local database.
# Store the photo in a directory and can be accessed via url.
@app.post("/pets")
def AddPets(type= _fastapi.Form(...),
            Gender= _fastapi.Form(...),
            size= _fastapi.Form(...),
            age= _fastapi.Form(...),
            # goodWithChildren=_fastapi.Form(...),
            file: _fastapi.UploadFile  = File(...),
            session:_orm.Session=_fastapi.Depends(get_session), 
             ):
    
    try:
        contents = file.file.read()
        with open("media/"+file.filename, 'wb') as media:
            media.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
    
    pets=_models.Pet(
                     type= type,
                     Gender= Gender,
                     size= size,
                     age= age,
                     photos=str("media/"+file.filename),     
                    #  goodWithChildren=goodWithChildren,
                    #  pet_have_owner=pets.have_owner,
                    )
    # pet_info=session.query(_models.Pet).filter(_models.Pet.photos==pets.pet_photo).first()

    session.add(pets)
    session.commit()
    session.refresh(pets)
    return {"status":"success",
            "petId":pets.petId}












#search endpoing
# Search local DB and also use petfinder animals endpoint to
@app.get("/pets{type}/{limit}")
def getPetsList(type:str,
                    #   gender:str,
                    #   size:str,
                    #   goodWithChildren:bool,
                      limit:int=3,
                      session:_orm.Session=_fastapi.Depends(get_session)):

    # /gender/{gender}/size/{size}/limit{limit}
    
    pet_collection=[]

    try:
        local_source_pets=session.query(_models.Pet).filter(_models.Pet.type==type,
                                                            # _models.Pet.Gender==gender,
                                                            # _models.Pet.size==size,
                                                            # _models.Pet.goodWithChildren==goodWithChildren,
                                                            # _models.Pet.pet_have_owner==False
                                                            ).limit(limit).all()
        
        remote_source_pets=_remote_api.pf.animal_types(type) 
        
        if local_source_pets is not None:
            pet_collection.append("Source:local database")
            pet_collection.append(local_source_pets)
         
        elif remote_source_pets is not None:
            pet_collection.append("source:remote API")
            pet_collection.append(remote_source_pets)
            session.add(pet_collection)
            session.commit()
            session.refresh(pet_collection)
            return pet_collection
           
        
    finally:
        return pet_collection


# get endpoint or list each pets 
@app.get("/pet_detail/{id}")
async def getPetsDetail(id:int,
                      session:_orm.Session=_fastapi.Depends(get_session),
                        status_code="you are successfull"
                        ):
    
    pets=session.query(_models.Pet).filter(_models.Pet.petId==id).first()
    return {'pet detail':pets}


# this is endpoint for add customers whose phones not exisit in database
@app.post("/customers")
def addCustomer(customer:_schemas.CreateCustomer,
                session:_orm.Session=_fastapi.Depends(get_session)):
    
    phone_number_check=session.query(_models.Customer).filter(_models.Customer.phone_number==customer.customer_phone).first()
    
    if phone_number_check is None :
                
        new_customer=_models.Customer(name=customer.customer_name,
                                    phone_number=customer.customer_phone,
                                    gender=customer.gender,
                                    petId=customer.petId)
          
        session.add(new_customer)
        session.commit()
        session.refresh(new_customer)
        return {'status' : 'success',
                'customerId':new_customer.customerId}
                
        
    else:
        return {"customer":"already exisit"}  



# get endpoint or list customers
@app.get("/customers")
async def getCustomer(skip:int=0,
                      limit:int=3,
                      session:_orm.Session=_fastapi.Depends(get_session)):
    
    customer=session.query(_models.Customer).order_by(_models.Customer.customerId).limit(limit).all()  
    return customer
   
   
# This endpoint will fetch all
# adoption requests in date range
# The lists should be ordered in
# descending order.
# i.e. the oldest requests appear at
# the top
import datetime
@app.get("/adoptions_request/{limit}")
def getAdoption(
                    #   fromDate:datetime.date.today(),
                    #   toDate:datetime.date.today(),
                      session:_orm.Session=_fastapi.Depends(get_session),
                      limit:int=10,
                      ):

    customer_adoption=session.query(_models.Customer).order_by(_models.Customer.adoption_request_date).limit(limit).all()
    # adoption_report_in_range=session.query(_models.Pet).filter(_models.Customer.adoption_request_date>=adoption.fromDate and 
    #                                                      _models.Customer.adoption_request_date<=adoption.toDate).limit(limit).all
   
    return {'data':customer_adoption}



        
# This endpoint will create an
# adoption record. This would mean
# that a customer has requested to
# adopt a pet.
@app.post("/adoptions")
def addAdoption(adoption:_schemas.Adoption,
                session:_orm.Session=_fastapi.Depends(get_session)):
    
    customer_check=session.query(_models.Customer).filter(_models.Customer.customerId==adoption.customerId).first()
    pet_check=session.query(_models.Pet).filter(_models.Pet.petId==adoption.petId).first()

    if customer_check is None or pet_check is None:
        raise _fastapi.HTTPException(status_code=404, detail="customerId or petId doesn't exisit")

        
    else:
        # adopton_request=session.query(_models.Pet).filter(_models.Pet.petId==adoption.petId).first()    
        adoption_request=_models.Customer(customerId=adoption.customerId,
                                            petId=adoption.petId)
        adoption_request.adoption_request_date==_date.datetime.utcnow                                    
        session.add(adoption_request)
        # session.commit()
        # session.refresh(adoption_request)
        return {'status':"success",
            'adoptionId':adoption_request.petId }
    
    
    
    
# This endpoint will create a small
# report using date range.




@app.post("/generateReport")
def generateReport(adoption:_schemas.Adoption,
                session:_orm.Session=_fastapi.Depends(get_session)):
    
    adoption_report=session.query(_models.Pet).filter(_models.Customer.adoption_request_date>=adoption.fromDate and 
                                                          _models.Customer.adoption_request_date<=adoption.toDate).count().all
   
    if adoption_report is not None:
       return {'status' : 'success','data':adoption_report }  
    else:

        raise _fastapi.HTTPException(status_code=404, detail="no exisiting adoption report ")

