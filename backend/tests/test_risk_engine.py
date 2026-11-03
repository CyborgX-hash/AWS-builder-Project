import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.risk_engine import DeterministicRiskEngine
from app.schemas.weather import WeatherSummary, CurrentWeather, DailyForecastItem, HourlyForecastItem
from app.schemas.risk import RiskLevel, RiskCategory

client = TestClient(app)


def create_mock_weather(
    temp_max: float = 30.0,
    daily_rain: float = 0.0,
    rain_days: int = 0
) -> WeatherSummary:
    """Helper to generate controlled meteorological scenarios."""
    daily_items = []
    for i in range(7):
        is_rain = i < rain_days
        daily_items.append(
            DailyForecastItem(
                date=f"2026-11-0{i+1}",
                temp_max=temp_max,
                temp_min=temp_max - 8.0,
                rainfall_sum=daily_rain if is_rain else 0.0,
                precipitation_probability_max=85 if is_rain else 10,
                weather_code=65 if is_rain else 1,
                weather_description="Heavy Rain" if is_rain else "Clear",
                et0_fao_evapotranspiration=4.5
            )
        )

    current = CurrentWeather(
        temperature=temp_max - 2.0,
        humidity=75.0 if daily_rain > 0 else 40.0,
        rainfall=daily_rain if rain_days > 0 else 0.0,
        wind_speed=12.0,
        rainfall_probability=85 if daily_rain > 0 else 10,
        weather_code=65 if daily_rain > 0 else 1,
        weather_description="Cloudy",
        time="2026-11-03T10:00"
    )

    return WeatherSummary(
        location="Balaghat, MP",
        latitude=21.8129,
        longitude=80.1838,
        current=current,
        daily=daily_items,
        hourly_next_24h=[],
        source="Test Mock Weather Model",
        retrieved_at="2026-11-03 10:00:00 IST"
    )


def test_heavy_rainfall_triggers_high_risk_for_soybean():
    # 70mm rain in first 2 days
    weather = create_mock_weather(temp_max=27.0, daily_rain=70.0, rain_days=2)
    report = DeterministicRiskEngine.calculate_risks(weather, "Soybean", "Flowering")

    assert report.crop == "Soybean"
    assert report.overall_risk_level == RiskLevel.HIGH

    rain_risk = next(a for a in report.assessments if a.category == RiskCategory.EXCESSIVE_RAINFALL)
    assert rain_risk.risk_level == RiskLevel.HIGH
    assert rain_risk.risk_score >= 70.0
    assert "Heavy rainfall alert" in rain_risk.reason_en
    assert "भारी वर्षा" in rain_risk.reason_hi


def test_heat_stress_triggers_high_risk():
    # 39°C max temperature (well above soybean 36°C critical limit)
    weather = create_mock_weather(temp_max=39.0, daily_rain=0.0, rain_days=0)
    report = DeterministicRiskEngine.calculate_risks(weather, "Soybean", "Flowering")

    heat_risk = next(a for a in report.assessments if a.category == RiskCategory.HEAT_STRESS)
    assert heat_risk.risk_level == RiskLevel.HIGH
    assert heat_risk.risk_score >= 75.0
    assert "pollen sterility" in heat_risk.reason_en
    assert "39.0°C" in heat_risk.reason_en


def test_dry_spell_and_water_stress_triggers_high_risk():
    # 7 dry days with 35°C
    weather = create_mock_weather(temp_max=35.0, daily_rain=0.0, rain_days=0)
    report = DeterministicRiskEngine.calculate_risks(weather, "Soybean", "Pod Development / Seed Filling")

    dry_risk = next(a for a in report.assessments if a.category == RiskCategory.DRY_SPELL)
    stress_risk = next(a for a in report.assessments if a.category == RiskCategory.WATER_STRESS)

    assert dry_risk.risk_level == RiskLevel.HIGH
    assert stress_risk.risk_level == RiskLevel.HIGH
    assert "Severe dry-spell alert" in dry_risk.reason_en


def test_rice_waterlogging_tolerance_vs_soybean():
    # 60mm rain over 3 days
    weather = create_mock_weather(temp_max=28.0, daily_rain=30.0, rain_days=2)
    
    soybean_report = DeterministicRiskEngine.calculate_risks(weather, "Soybean", "Vegetative")
    rice_report = DeterministicRiskEngine.calculate_risks(weather, "Rice", "Tillering")

    soybean_wl = next(a for a in soybean_report.assessments if a.category == RiskCategory.WATERLOGGING)
    rice_wl = next(a for a in rice_report.assessments if a.category == RiskCategory.WATERLOGGING)

    # 60mm rain causes High risk in Soybean, but Rice tolerates standing water (Moderate or Low)
    assert soybean_wl.risk_level == RiskLevel.HIGH
    assert rice_wl.risk_level in [RiskLevel.LOW, RiskLevel.MODERATE]


def test_mild_favorable_weather_returns_low_risk():
    # 19°C (optimal for wheat tillering) and 5mm light shower
    weather = create_mock_weather(temp_max=19.0, daily_rain=5.0, rain_days=1)
    report = DeterministicRiskEngine.calculate_risks(weather, "Wheat", "Tillering & Jointing")

    heat_risk = next(a for a in report.assessments if a.category == RiskCategory.HEAT_STRESS)
    rain_risk = next(a for a in report.assessments if a.category == RiskCategory.EXCESSIVE_RAINFALL)

    assert heat_risk.risk_level == RiskLevel.LOW
    assert rain_risk.risk_level == RiskLevel.LOW


def test_api_risk_report():
    response = client.get("/api/risk/report?crop=Soybean&growth_stage=Flowering&location=Balaghat")
    assert response.status_code == 200
    data = response.json()
    assert data["crop"] == "Soybean"
    assert "overall_risk_level" in data
    assert len(data["assessments"]) == 5
    assert "limitations_disclaimer" in data
