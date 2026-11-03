from typing import Dict, Any
from strands import tool
from app.services.weather_service import WeatherService
from app.services.risk_engine import DeterministicRiskEngine


@tool
async def evaluate_climate_risks(
    latitude: float,
    longitude: float,
    crop_name: str,
    growth_stage: str,
    location_name: str = "Farm Location"
) -> Dict[str, Any]:
    """
    Execute the deterministic agricultural climate-risk engine for a crop at a specific location.
    
    Args:
        latitude: Latitude of the farm.
        longitude: Longitude of the farm.
        crop_name: Crop name (Soybean, Rice, Wheat, Maize, Cotton).
        growth_stage: Growth stage (e.g. Flowering, Vegetative, Grain Filling).
        location_name: Human-readable location name.
        
    Returns:
        Structured risk report containing numerical scores, categories, explanations, and monitoring tips.
    """
    weather = await WeatherService.get_forecast(latitude, longitude, location_name)
    report = DeterministicRiskEngine.calculate_risks(weather, crop_name, growth_stage)
    return report.model_dump()

