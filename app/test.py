# import fastapi as _fastapi
import pytest

from app.main import app


client=_fastapi.testclient.TestClient(app)

def test_add_pet():
    data={"type":"cat",
        "gender":"male",
        "size":"small",
        "age":"young",
        "photo":"/insa.jpg"
        
        }
    response = client.get("/pets",json=data)
  
    assert response.status_code == 200
    assert data in response.json()
    # assert response.json() == {"msg": "Hello World"}