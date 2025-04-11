from pydantic import BaseModel
from typing import Union
class Car(BaseModel):
    make: str
    model: str
    year: int
    price: int
    mileage: Union[int, str]  
    engine_type: str
    engine_volume: float
    transmission: str
    location: str
    image_url: str
