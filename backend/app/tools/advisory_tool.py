from typing import Dict, Any
from strands import tool
from app.services.weather_service import WeatherService
from app.services.risk_engine import DeterministicRiskEngine
from app.services.advisory_service import AdvisoryService


@tool
async def generate_farming_advisory(
    latitude: float,
    longitude: float,
    crop_name: str,
    growth_stage: str,
    preferred_language: str = "en",
    location_name: str = "Farm Location"
) -> Dict[str, Any]:
    """
    Generate practical, preventive agricultural advisories and a 3-day farming action plan.
    
    Args:
        latitude: Latitude coordinate.
        longitude: Longitude coordinate.
        crop_name: Name of crop (e.g. 'Soybean', 'Wheat').
        growth_stage: Current growth stage.
        preferred_language: Preferred response language ('en' for English, 'hi' for Hindi).
        location_name: Name of the location.
        
    Returns:
        Structured advisory response containing immediate precautions, 3-day action plans, and official disclaimer.
    """
    weather = await WeatherService.get_forecast(latitude, longitude, location_name)
    risk_report = DeterministicRiskEngine.calculate_risks(weather, crop_name, growth_stage)
    advisory = AdvisoryService.generate_advisory(risk_report, weather, preferred_language)
    return advisory.model_dump()

