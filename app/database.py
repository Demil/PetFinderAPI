
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os
from dotenv import load_dotenv

load_dotenv()
Database_URL="postgresql://"+os.getenv("USER_NAME")+":"+os.getenv("DATABASE_PASSWORD")+"@localhost/"+os.getenv("DATABASE")
engine=create_engine(Database_URL)

Base=declarative_base()


SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)







