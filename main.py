import os
from typing import List

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import models.location as models
import schemas.schemas as schemas
import services.weather as weather
from database.database import get_db, engine
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Weather API is running"}

@app.get("/locations", response_model=List[schemas.LocationWithWeather])
def get_locations(db: Session = Depends(get_db)):
    """Get all locations with current weather data"""
    locations = db.query(models.Location).all()
    
    result = []
    for location in locations:
        # Get current weather for location
        current_weather = weather.get_current_weather(location.latitude, location.longitude)
        
        # Combine location and weather data
        location_with_weather = schemas.LocationWithWeather(
            id=location.id,
            name=location.name,
            latitude=location.latitude,
            longitude=location.longitude,
            temperature=current_weather.get("temperature", 0),
            rainfall=current_weather.get("rainfall", 0),
            weather_code=current_weather.get("weather_code", 0),
        )
        result.append(location_with_weather)
    
    return result

@app.post("/locations", response_model=schemas.Location)
def create_location(location: schemas.LocationCreate, db: Session = Depends(get_db)):
    """Add a new location"""
    existing_location = db.query(models.Location).filter(models.Location.name == location.name).first()
    if existing_location:
        raise HTTPException(status_code=403, detail="Location already exists")
    
    db_location = models.Location(
        name=location.name,
        latitude=location.latitude,
        longitude=location.longitude
    )
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

@app.delete("/locations/{location_id}", response_model=schemas.Location)
def delete_location(location_id: int, db: Session = Depends(get_db)):
    """Delete a location by ID"""
    location = db.query(models.Location).filter(models.Location.id == location_id).first()
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    
    db.delete(location)
    db.commit()
    return location

@app.get("/forecast/{location_id}", response_model=schemas.Forecast)
def get_forecast(location_id: int, db: Session = Depends(get_db)):
    """Get 7-day forecast for a location"""
    location = db.query(models.Location).filter(models.Location.id == location_id).first()
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    
    # Get forecast from OpenMeteo
    forecast_data = weather.get_forecast(location.latitude, location.longitude)
    
    # Transform data to match schema
    forecast = schemas.Forecast(
        location_id=location.id,
        location_name=location.name,
        days=forecast_data
    )
    
    return forecast

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
