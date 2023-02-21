from sqlalchemy import Column, Integer, String, Boolean,Date,ForeignKey
from sqlalchemy_utils import URLType
import datetime as _date
import sqlalchemy as _sql
import app.database as _database
import sqlalchemy.orm as _orm
from furl import furl
from fastapi import File,UploadFile


class Pet(_database.Base):
    
    __tablename__ ='pet_table'
    
    petId = Column(Integer,primary_key = True, index=True)
    age = Column(String(50),default="local")
    type = Column(String,nullable=False)
    Gender = Column(String(6),nullable=False)
    size = Column(String(50),nullable = False)
    goodWithChildren = Column(Boolean(),default=False)
    photos=Column(URLType)
    adoption_status = Column(Boolean(),default= False,index=True)
    customer_to_pet_relation=_orm.relationship("Customer",back_populates="pet_to_customer_relation")

    
    
    
class Customer(_database.Base):
    __tablename__ ='customer_table'
    
    customerId = Column(Integer,primary_key = True,index=True)
    petId =  Column(Integer,ForeignKey(Pet.petId))
    name = Column(String,nullable= False,index=True)
    phone_number = Column(Integer,nullable=False,index=True,unique=True)
    gender = Column(String,nullable=False)
    adoption_request_date=_sql.Column(_sql.DateTime,default=_date.datetime.utcnow)
    pet_to_customer_relation=_orm.relationship("Pet",back_populates="customer_to_pet_relation")

# class Customer_Pet_Adoption(_database.Base):
#     __tablename__ ='pet_adoption_request_table'
    
#     pet_adoption_id = Column(Integer,primary_key = True,index=True)
    
#     adoption_request_approval = Column(Boolean(),default= True,index=True)
#     adoption_request_date=_sql.Column(_sql.DateTime,default=_date.datetime.utcnow)
#     adopted_pet_info=_orm.relationship("Pet",back_populates="adoption_info")
    
#     customerId =  Column(Integer,ForeignKey(Customer.customerId))
#     owner=_orm.relationship("Customer",back_populates="adoption")
   