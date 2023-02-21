import app.database as _database
# import models as _models
# import schemas as _schemas

def manage_table():
    return _database.Base.metadata.create_all(bind=_database.engine)

 
        
        
# async def create_pet(pet:_schemas.CreatePet,db:"Session"):
#     pet=_models.Pet(**pet.dict())
#     db.add(pet)
#     db.commit()
#     db.refresh(pet) 
#     return _schemas._Pet.from_orm(pet)       