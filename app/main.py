from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Depends, Query
from pymongo import MongoClient
from typing import List
from .models import Car
from .scraper import scrape_cars
from .auth import get_current_user, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/")
async def root():
    return FileResponse("static/index.html")
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != "test" or form_data.password != "password":
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    # Генерація токену
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Підключення до MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['car_db']
car_collection = db['cars']

@app.on_event("startup")
async def startup_db():
    # Підключення до бази даних
    pass

@app.post("/cars", response_model=Car)
async def create_car(car: Car):
    # Перевірка на наявність такого автомобіля
    existing_car = car_collection.find_one({"make": car.make, "model": car.model, "year": car.year})
    if existing_car:
        raise HTTPException(status_code=400, detail="Car already exists")
    car_dict = car.model_dump()
    car_collection.insert_one(car_dict)
    return car

@app.get("/cars", response_model=List[Car])
async def get_cars(
    skip: int = 0,
    limit: int = 10,
    min_price: float = Query(None, ge=0),
    max_price: float = Query(None, ge=0),
    min_mileage: int = Query(None, ge=0),
    max_mileage: int = Query(None, ge=0),
    sort_by: str = Query("price", enum=["price", "year", "mileage"]),
    sort_order: str = Query("asc", enum=["asc", "desc"]),
):
    query = {}
    if min_price is not None:
        query["price"] = {"$gte": min_price}
    if max_price is not None:
        query["price"] = {"$lte": max_price}
    if min_mileage is not None:
        query["mileage"] = {"$gte": min_mileage}
    if max_mileage is not None:
        query["mileage"] = {"$lte": max_mileage}
    
    sort_order = 1 if sort_order == "asc" else -1
    cars = list(car_collection.find(query).skip(skip).limit(limit).sort(sort_by, sort_order))
    return cars

@app.get("/cars/{car_id}", response_model=Car)
async def get_car(car_id: str):
    car = car_collection.find_one({"_id": car_id})
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car

@app.get("/cars/make/{make}", response_model=List[Car])
async def get_cars_by_make(make: str):
    cars = list(car_collection.find({"make": make}))
    return cars

@app.get("/cars/year/{year}", response_model=List[Car])
async def get_cars_by_year(year: int):
    cars = list(car_collection.find({"year": year}))
    return cars

@app.put("/cars/{car_id}", response_model=Car)
async def update_car(car_id: str, car: Car):
    result = car_collection.update_one({"_id": car_id}, {"$set": car.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Car not found")
    return car

@app.delete("/cars/{car_id}")
async def delete_car(car_id: str):
    result = car_collection.delete_one({"_id": car_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Car not found")
    return {"message": "Car deleted"}

@app.get("/scrape")
async def scrape_and_save():
    cars = scrape_cars()
    new_count = 0
    
    car_collection.delete_many({})
    
    for car in cars:
        car_collection.insert_one(car)
        new_count += 1
        
    return {"message": f"Scraped and saved {new_count} new cars"}
