from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
import datetime

from app.config import settings
from app.database.session import get_db
from app.database.models import Farmer, CropProfile, WeatherRecord, RiskReport, Advisory
from app.schemas.farmer import FarmerCreate, FarmerOut, AdvisoryGenerateRequest
from app.schemas.weather import WeatherSummary, LocationCoordinates
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.weather_service import WeatherService
from app.services.advisory_service import AdvisoryService
from app.agents.orchestrator import KrishiOrchestrator

router = APIRouter()
orchestrator_instance = KrishiOrchestrator()


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    """Interactive multi-agent chat endpoint supporting Hindi and English."""
    response = await orchestrator_instance.execute_advisory_pipeline(
        query=request.query,
        location=request.location,
        crop=request.crop,
        growth_stage=request.growth_stage,
        language=request.language,
        lat=request.latitude,
        lon=request.longitude
    )

    # Persist advisory record to SQLite history
    try:
        advisory_entry = Advisory(
            crop=response.extracted_entities.get("crop"),
            recommendation=response.response[:1000],
            language=response.language
        )
        db.add(advisory_entry)
        db.commit()
    except Exception as e:
        db.rollback()

    return response


@router.post("/advisory/generate")
async def generate_advisory_endpoint(req: AdvisoryGenerateRequest, db: Session = Depends(get_db)):
    """Direct structured advisory generation for selected crop and location."""
    response = await orchestrator_instance.execute_advisory_pipeline(
        query=f"Provide detailed agricultural advisory for {req.crop} at {req.growth_stage} in {req.location}",
        location=req.location,
        crop=req.crop,
        growth_stage=req.growth_stage,
        language=req.language or "en",
        lat=req.latitude,
        lon=req.longitude
    )
    return response.structured_data.get("advisory") if response.structured_data else {}


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


@router.get("/risk/report")
async def get_risk_report_endpoint(
    crop: str = Query("Soybean", description="Crop name"),
    growth_stage: str = Query("Flowering", description="Crop growth stage"),
    location: Optional[str] = Query("Balaghat", description="Location name"),
    lat: Optional[float] = Query(None),
    lon: Optional[float] = Query(None)
):
    """Generate deterministic climate risk report for a crop and location."""
    from app.services.risk_engine import DeterministicRiskEngine
    if lat is None or lon is None:
        coords = await WeatherService.resolve_coordinates(location or "Balaghat")
        lat, lon = coords.latitude, coords.longitude
        location = coords.name

    weather = await WeatherService.get_forecast(lat, lon, location)
    report = DeterministicRiskEngine.calculate_risks(weather, crop, growth_stage)
    return report


@router.get("/crops")
def list_crops():
    """List all supported crops with localized names and stage descriptions."""
    from app.tools.crop_tool import load_crop_knowledge
    data = load_crop_knowledge()
    crops_summary = []
    for k, v in data.get("crops", {}).items():
        crops_summary.append({
            "key": k,
            "crop_name": v["crop_name"],
            "crop_name_hi": v["crop_name_hi"],
            "category": v["category"],
            "stages": [s["stage_name"] for s in v["growth_stages"]],
            "stages_hi": [s["stage_name_hi"] for s in v["growth_stages"]],
            "references": v.get("sourced_references", [])
        })
    return crops_summary


@router.get("/crops/{crop_name}")
def get_crop_details(crop_name: str):
    """Get complete agronomic profile and stage thresholds for a specific crop."""
    from app.tools.crop_tool import get_crop_profile
    result = get_crop_profile(crop_name)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


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
