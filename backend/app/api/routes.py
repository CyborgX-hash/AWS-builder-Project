from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
import datetime

from app.config import settings
from app.database.session import get_db
from app.database.models import Farmer, CropProfile, WeatherRecord, RiskReport, Advisory
from app.schemas.farmer import FarmerCreate, FarmerOut
from app.schemas.weather import WeatherSummary, LocationCoordinates
from app.services.weather_service import WeatherService

router = APIRouter()


@router.get("/health")
def health_check():
    """Health check endpoint providing service status and timestamp."""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "environment": settings.ENVIRONMENT
    }


@router.get("/weather/coordinates", response_model=LocationCoordinates)
async def get_coordinates(location: str = Query(..., description="Indian village, town, or district")):
    """Resolve location name to latitude and longitude."""
    return await WeatherService.resolve_coordinates(location)


@router.get("/weather/current")
async def get_current_weather_endpoint(
    lat: Optional[float] = Query(None),
    lon: Optional[float] = Query(None),
    location: Optional[str] = Query(None)
):
    """Retrieve current weather observation for a location."""
    if lat is None or lon is None:
        if not location:
            raise HTTPException(status_code=400, detail="Must provide either (lat, lon) or location name.")
        coords = await WeatherService.resolve_coordinates(location)
        lat, lon = coords.latitude, coords.longitude
        location = coords.name

    summary = await WeatherService.get_forecast(lat, lon, location or "Farm Location")
    return {
        "location": summary.location,
        "latitude": summary.latitude,
        "longitude": summary.longitude,
        "current": summary.current,
        "retrieved_at": summary.retrieved_at,
        "source": summary.source
    }


@router.get("/weather/forecast", response_model=WeatherSummary)
async def get_weather_forecast_endpoint(
    lat: Optional[float] = Query(None),
    lon: Optional[float] = Query(None),
    location: Optional[str] = Query(None)
):
    """Retrieve 7-day daily forecast and 24h hourly forecast."""
    if lat is None or lon is None:
        if not location:
            location = "Balaghat"
        coords = await WeatherService.resolve_coordinates(location)
        lat, lon = coords.latitude, coords.longitude
        location = coords.name

    return await WeatherService.get_forecast(lat, lon, location or "Farm Location")


@router.post("/farmer/profile", response_model=FarmerOut)
def create_farmer_profile(farmer_in: FarmerCreate, db: Session = Depends(get_db)):
    """Store or register a farmer's location and preferred crop profile."""
    farmer = Farmer(
        name=farmer_in.name,
        preferred_language=farmer_in.preferred_language,
        location=farmer_in.location,
        latitude=farmer_in.latitude,
        longitude=farmer_in.longitude
    )
    db.add(farmer)
    db.commit()
    db.refresh(farmer)

    if farmer_in.crop_name and farmer_in.growth_stage:
        crop_profile = CropProfile(
            crop_name=farmer_in.crop_name,
            growth_stage=farmer_in.growth_stage,
            farmer_id=farmer.id
        )
        db.add(crop_profile)
        db.commit()

    return farmer


@router.get("/farmer/history")
def get_farmer_history(farmer_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    """Fetch previous risk reports and advisories for a farmer or recent records."""
    query = db.query(Advisory)
    if farmer_id:
        query = query.filter(Advisory.farmer_id == farmer_id)
    advisories = query.order_by(Advisory.created_at.desc()).limit(10).all()

    return [
        {
            "id": a.id,
            "crop": a.crop,
            "recommendation": a.recommendation,
            "language": a.language,
            "created_at": a.created_at.isoformat() if a.created_at else None
        }
        for a in advisories
    ]
