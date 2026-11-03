import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.weather_service import WeatherService, INDIAN_AGRI_DISTRICTS


client = TestClient(app)


def test_resolve_known_district():
    lat, lon, state = INDIAN_AGRI_DISTRICTS["balaghat"]
    assert lat == 21.8129
    assert lon == 80.1838
    assert state == "Madhya Pradesh"


@pytest.mark.asyncio
async def test_resolve_coordinates_service():
    coords = await WeatherService.resolve_coordinates("Balaghat")
    assert coords.name == "Balaghat"
    assert coords.latitude == 21.8129
    assert coords.longitude == 80.1838
    assert coords.state == "Madhya Pradesh"


def test_get_weather_coordinates_api():
    response = client.get("/api/weather/coordinates?location=Balaghat")
    assert response.status_code == 200
    data = response.json()
    assert data["latitude"] == 21.8129
    assert data["longitude"] == 80.1838


def test_get_current_weather_api():
    response = client.get("/api/weather/current?location=Balaghat")
    assert response.status_code == 200
    data = response.json()
    assert "current" in data
    assert "temperature" in data["current"]
    assert "humidity" in data["current"]
    assert "rainfall" in data["current"]
    assert data["location"] == "Balaghat"


def test_get_weather_forecast_api():
    response = client.get("/api/weather/forecast?lat=21.8129&lon=80.1838&location=Balaghat")
    assert response.status_code == 200
    data = response.json()
    assert len(data["daily"]) == 7
    assert len(data["hourly_next_24h"]) == 24
    assert data["current"]["temperature"] is not None
    assert "Open-Meteo" in data["source"] or "Agro-Meteorological" in data["source"]

