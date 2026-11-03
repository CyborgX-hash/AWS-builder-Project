from strands import tool
from typing import Dict, Any
from app.services.weather_service import WeatherService


@tool
async def get_current_weather(latitude: float, longitude: float, location_name: str = "Farm") -> Dict[str, Any]:
    """
    Retrieve real-time current weather observations for a farmer's location.
    
    Args:
        latitude: Latitude of the farm location.
        longitude: Longitude of the farm location.
        location_name: Optional name of the location.
        
    Returns:
        Current temperature, humidity, rainfall, wind speed, weather code, and description.
    """
    summary = await WeatherService.get_forecast(latitude, longitude, location_name)
    return {
        "location": summary.location,
        "temperature_c": summary.current.temperature,
        "humidity_percent": summary.current.humidity,
        "rainfall_mm": summary.current.rainfall,
        "wind_speed_kmh": summary.current.wind_speed,
        "rainfall_probability": summary.current.rainfall_probability,
        "weather_description": summary.current.weather_description,
        "observation_time": summary.current.time,
        "data_source": summary.source
    }


@tool
async def get_weather_forecast(latitude: float, longitude: float, location_name: str = "Farm") -> Dict[str, Any]:
    """
    Retrieve 7-day daily agricultural forecast and next 24-hour rainfall trends.
    
    Args:
        latitude: Latitude of the farm location.
        longitude: Longitude of the farm location.
        location_name: Optional name of the location.
        
    Returns:
        Structured 7-day daily forecast and 24-hour trends with precipitation probability and temperature ranges.
    """
    summary = await WeatherService.get_forecast(latitude, longitude, location_name)
    daily_list = [
        {
            "date": d.date,
            "temp_max_c": d.temp_max,
            "temp_min_c": d.temp_min,
            "rainfall_sum_mm": d.rainfall_sum,
            "precip_probability_max": d.precipitation_probability_max,
            "weather": d.weather_description,
            "evapotranspiration_mm": d.et0_fao_evapotranspiration
        }
        for d in summary.daily
    ]
    return {
        "location": summary.location,
        "daily_forecast_7d": daily_list,
        "retrieved_at": summary.retrieved_at,
        "data_source": summary.source
    }

