from strands import tool
from typing import Dict, Any
from app.services.weather_service import WeatherService


@tool
async def get_location_coordinates(location_name: str) -> Dict[str, Any]:
    """
    Resolve any village, block, district, or town in India to its latitude and longitude coordinates.
    
    Args:
        location_name: Name of the Indian village, district, or town (e.g. 'Balaghat', 'Indore', 'Nagpur').
        
    Returns:
        Dictionary containing resolved name, latitude, longitude, and state.
    """
    coords = await WeatherService.resolve_coordinates(location_name)
    return {
        "name": coords.name,
        "latitude": coords.latitude,
        "longitude": coords.longitude,
        "state": coords.state,
        "country": coords.country
    }

