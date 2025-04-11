from fastapi.testclient import TestClient
from app.main import app
import random
import time
client = TestClient(app)

def test_create_car():
    response = client.post("/cars", json={
        "make": "Toyota", "model": f"Camry-{int(time.time())}",
        "year": 2020, "price": 20000, "mileage": "10000",
        "engine_type": "Petrol", "engine_volume": 2.5,
        "transmission": "Automatic", "location": "NY",
        "image_url": "url"
    })
    print(response.json()) 
    assert response.status_code == 200
    assert response.json()["make"] == "Toyota"


def test_get_cars():
    response = client.get("/cars")
    assert response.status_code == 200
    assert len(response.json()) > 0
