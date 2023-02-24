# library for remotePetFinder Api
import petpy
import os
from dotenv import load_dotenv

load_dotenv()
pf = petpy.Petfinder(key=os.getenv("API_KEY"), 
                    secret=os.getenv("API_SECRETE"))
