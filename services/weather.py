import os
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any
from dotenv import load_dotenv
load_dotenv()

url = os.getenv('WEATHER_API')

def get_current_weather(latitude: float, longitude: float) -> Dict[str, Any]:
    """
    Get current weather for a location using OpenMeteo API
    
    Args:
        latitude: Location latitude
        longitude: Location longitude
        
    Returns:
        Dictionary with current weather data
    """
    
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": ["temperature_2m", "precipitation", "weather_code"],
        "timezone": "auto"
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Extract current weather data
        current = data.get("current", {})
        
        return {
            "temperature": current.get("temperature_2m", 0),
            "rainfall": current.get("precipitation", 0),
            "weather_code": current.get("weather_code", 0)
        }
    except Exception as e:
        print(f"Error fetching current weather: {e}")
        return {
            "temperature": 0,
            "rainfall": 0,
            "weather_code": 0
        }

def get_forecast(latitude: float, longitude: float) -> List[Dict[str, Any]]:
    """
    Get 7-day forecast for a location using OpenMeteo API
    
    Args:
        latitude: Location latitude
        longitude: Location longitude
        
    Returns:
        List of dictionaries with forecast data for each day
    """
    
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
        "timezone": "auto",
        "forecast_days": 7
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Extract daily forecast data
        daily = data.get("daily", {})
        dates = daily.get("time", [])
        forecast_days = []
        for i in range(min(7, len(daily.get("time", [])))):

            date_obj = datetime.strptime(dates[i], "%Y-%m-%d")
            day_name = date_obj.strftime("%A")

            forecast_days.append({
                "date": daily.get("time", [])[i],
                "day_name": day_name,
                "weather_code": daily.get("weather_code", [])[i],
                "min_temperature": daily.get("temperature_2m_min", [])[i],
                "max_temperature": daily.get("temperature_2m_max", [])[i],
                "rainfall": daily.get("precipitation_sum", [])[i]
            })
        
        return forecast_days
    except Exception as e:
        print(f"Error fetching forecast: {e}")
        # Return empty forecast if there's an error
        today = datetime.now()
        return [
            {
                "date": (today + timedelta(days=i)).strftime("%Y-%m-%d"),
                "weather_code": 0,
                "min_temperature": 0,
                "max_temperature": 0,
                "rainfall": 0
            }
            for i in range(7)
        ]
