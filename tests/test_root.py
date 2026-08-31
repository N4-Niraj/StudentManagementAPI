from fastapi.testclient import TestClient

from app.main import app

'''creates a fake HTTP client that can communicate with your FastAPI 
application without you having to run Uvicorn.'''

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Student Management API"}