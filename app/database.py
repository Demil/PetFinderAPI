# import sqlalchemy as _sql
# from sqlalchemy.orm import sessionmaker
# import sqlalchemy.ext.declarative as _declarative
# import sqlalchemy.orm as _orm



from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Database_URL="postgresql://demilew:Demian752728@localhost/pet_db"
engine=create_engine(Database_URL)

Base=declarative_base()


SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)





# def get_db():
#     db=_database.SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()  






