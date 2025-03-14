from typing import List, Optional
from pydantic import BaseModel

class LocationBase(BaseModel):
    """Base schema for location data"""
    name: str
    latitude: float
    longitude: float

class LocationCreate(LocationBase):
    """Schema for creating a new location"""
    pass

class Location(LocationBase):
    """Schema for location with ID"""
    id: int

    class Config:
        orm_mode = True

class LocationWithWeather(Location):
    """Schema for location with current weather data"""
    temperature: float
    rainfall: float
    weather_code: int

class ForecastDay(BaseModel):
    """Schema for a single day in the forecast"""
    date: str
    day_name: str
    weather_code: int
    min_temperature: float
    max_temperature: float
    rainfall: float

class Forecast(BaseModel):
    """Schema for a 7-day forecast"""
    location_id: int
    location_name: str
    days: List[ForecastDay]
