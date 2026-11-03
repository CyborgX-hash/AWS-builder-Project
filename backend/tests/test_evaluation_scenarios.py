import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.risk_engine import DeterministicRiskEngine
from app.services.weather_service import WeatherService
from app.schemas.weather import WeatherSummary, CurrentWeather, DailyForecastItem
from app.schemas.risk import RiskLevel, RiskCategory
from app.agents.orchestrator import KrishiOrchestrator

client = TestClient(app)


def build_scenario_weather(
    loc_name: str,
    temp_max: float,
    temp_min: float,
    daily_rain_list: list[float],
    precip_prob_list: list[int]
) -> WeatherSummary:
    daily_items = []
    for i in range(7):
        r = daily_rain_list[i] if i < len(daily_rain_list) else 0.0
        p = precip_prob_list[i] if i < len(precip_prob_list) else 10
        daily_items.append(
            DailyForecastItem(
                date=f"2026-11-{i+1:02d}",
                temp_max=temp_max,
                temp_min=temp_min,
                rainfall_sum=r,
                precipitation_probability_max=p,
                weather_code=65 if r >= 20.0 else (61 if r > 0 else 1),
                weather_description="Heavy Rain" if r >= 20.0 else ("Light Rain" if r > 0 else "Clear"),
                et0_fao_evapotranspiration=4.2
            )
        )

    current = CurrentWeather(
        temperature=temp_max - 3.0,
        humidity=80.0 if sum(daily_rain_list[:2]) > 10 else 45.0,
        rainfall=daily_rain_list[0] if daily_rain_list else 0.0,
        wind_speed=14.0,
        rainfall_probability=precip_prob_list[0] if precip_prob_list else 10,
        weather_code=65 if (daily_rain_list and daily_rain_list[0] >= 20) else 1,
        weather_description="Cloudy" if daily_rain_list and daily_rain_list[0] > 0 else "Fair",
        time="2026-11-03T11:00"
    )

    return WeatherSummary(
        location=loc_name,
        latitude=21.8129,
        longitude=80.1838,
        current=current,
        daily=daily_items,
        hourly_next_24h=[],
        source="Evaluation Scenario Generator",
        retrieved_at="2026-11-03 11:00:00 IST"
    )


# Scenario 1: Heavy rainfall (85mm/48h) on Soybean at Flowering
def test_scenario_1_heavy_rain_soybean_flowering():
    w = build_scenario_weather("Balaghat", 27.0, 21.0, [45.0, 40.0, 5.0, 0.0, 0.0, 0.0, 0.0], [90, 85, 40, 10, 10, 10, 10])
    rep = DeterministicRiskEngine.calculate_risks(w, "Soybean", "Flowering")
    rain_risk = next(a for a in rep.assessments if a.category == RiskCategory.EXCESSIVE_RAINFALL)
    assert rain_risk.risk_level == RiskLevel.HIGH
    assert rain_risk.risk_score >= 80.0


# Scenario 2: Extreme heatwave (42°C) on Maize at Tasseling/Silking
def test_scenario_2_heatwave_maize_silking():
    w = build_scenario_weather("Chhindwara", 42.0, 28.0, [0.0]*7, [5]*7)
    rep = DeterministicRiskEngine.calculate_risks(w, "Maize", "Tasseling & Silking")
    heat_risk = next(a for a in rep.assessments if a.category == RiskCategory.HEAT_STRESS)
    assert heat_risk.risk_level == RiskLevel.HIGH
    assert heat_risk.risk_score >= 85.0
    assert "critical threshold" in heat_risk.reason_en


# Scenario 3: Extended dry spell (7 dry days, 36°C) on Soybean at Pod Development
def test_scenario_3_dry_spell_soybean_pod_filling():
    w = build_scenario_weather("Seoni", 36.0, 24.0, [0.0]*7, [5]*7)
    rep = DeterministicRiskEngine.calculate_risks(w, "Soybean", "Pod Development / Seed Filling")
    dry_risk = next(a for a in rep.assessments if a.category == RiskCategory.DRY_SPELL)
    assert dry_risk.risk_level == RiskLevel.HIGH
    assert dry_risk.relevant_weather_variables["consecutive_dry_days"] == 7


# Scenario 4: Continuous standing water on Cotton at Vegetative stage
def test_scenario_4_waterlogging_cotton():
    w = build_scenario_weather("Amravati", 28.0, 22.0, [30.0, 35.0, 25.0, 5.0, 0.0, 0.0, 0.0], [80, 80, 75, 20, 10, 10, 10])
    rep = DeterministicRiskEngine.calculate_risks(w, "Cotton", "Vegetative / Square Formation")
    wl_risk = next(a for a in rep.assessments if a.category == RiskCategory.WATERLOGGING)
    assert wl_risk.risk_level == RiskLevel.HIGH


# Scenario 5: Flash flood on young Rice / Paddy at Nursery stage
def test_scenario_5_flash_flood_rice_nursery():
    w = build_scenario_weather("Raipur", 26.0, 21.0, [60.0, 50.0, 40.0, 0.0, 0.0, 0.0, 0.0], [90, 85, 80, 10, 10, 10, 10])
    rep = DeterministicRiskEngine.calculate_risks(w, "Rice", "Nursery / Seedling")
    wl_risk = next(a for a in rep.assessments if a.category == RiskCategory.WATERLOGGING)
    assert wl_risk.risk_level == RiskLevel.HIGH
    assert "Submergence" in wl_risk.reason_en


# Scenario 6: Moderate rain on Rice at Tillering stage (Paddy flood tolerance)
def test_scenario_6_moderate_water_rice_tillering():
    w = build_scenario_weather("Cuttack", 29.0, 23.0, [20.0, 20.0, 10.0, 0.0, 0.0, 0.0, 0.0], [60, 60, 40, 10, 10, 10, 10])
    rep = DeterministicRiskEngine.calculate_risks(w, "Rice", "Tillering")
    wl_risk = next(a for a in rep.assessments if a.category == RiskCategory.WATERLOGGING)
    assert wl_risk.risk_level in [RiskLevel.LOW, RiskLevel.MODERATE]


# Scenario 7: Unseasonal rain on Wheat at Maturity / Harvest
def test_scenario_7_unseasonal_rain_wheat_harvest():
    w = build_scenario_weather("Ludhiana", 25.0, 16.0, [30.0, 25.0, 0.0, 0.0, 0.0, 0.0, 0.0], [80, 75, 10, 10, 10, 10, 10])
    rep = DeterministicRiskEngine.calculate_risks(w, "Wheat", "Maturity / Harvest")
    rain_risk = next(a for a in rep.assessments if a.category == RiskCategory.EXCESSIVE_RAINFALL)
    assert rain_risk.risk_level == RiskLevel.HIGH


# Scenario 8: Terminal heat stress on Wheat during Milking & Dough stage
def test_scenario_8_terminal_heat_wheat_dough():
    w = build_scenario_weather("Karnal", 34.0, 20.0, [0.0]*7, [10]*7)
    rep = DeterministicRiskEngine.calculate_risks(w, "Wheat", "Milking & Dough (Grain Filling)")
    heat_risk = next(a for a in rep.assessments if a.category == RiskCategory.HEAT_STRESS)
    assert heat_risk.risk_level == RiskLevel.HIGH


# Scenario 9: Ideal weather for Wheat at Tillering
def test_scenario_9_ideal_conditions_wheat_tillering():
    # 22mm well-distributed rain meets weekly water need (28mm), keeping deficit <10mm (LOW risk)
    w = build_scenario_weather("Ludhiana", 19.0, 8.0, [5.0, 5.0, 4.0, 4.0, 4.0, 0.0, 0.0], [40, 40, 30, 30, 30, 10, 10])
    rep = DeterministicRiskEngine.calculate_risks(w, "Wheat", "Tillering & Jointing")
    assert rep.overall_risk_level == RiskLevel.LOW


# Scenario 10: Invalid crop name input handled safely
def test_scenario_10_invalid_crop_handling():
    res = client.get("/api/crops/dragonfruit")
    assert res.status_code == 404
    assert "not currently in the primary knowledge base" in res.json()["detail"]


# Scenario 11: Missing location fallback
@pytest.mark.asyncio
async def test_scenario_11_missing_location_fallback():
    coords = await WeatherService.resolve_coordinates("")
    assert coords.name == "Balaghat"
    assert coords.latitude == 21.8129


# Scenario 12: Offline fallback weather generator resilience
def test_scenario_12_weather_fallback():
    fallback = WeatherService._generate_fallback_summary("Remote Farm", 22.0, 78.0)
    assert fallback.location == "Remote Farm"
    assert len(fallback.daily) == 7
    assert len(fallback.hourly_next_24h) == 24


# Scenario 13: Full bilingual chat Hindi query execution
@pytest.mark.asyncio
async def test_scenario_13_hindi_chat():
    orch = KrishiOrchestrator()
    resp = await orch.execute_advisory_pipeline(
        query="क्या सीहोरा में कल बारिश से सोयाबीन में नुकसान होगा?",
        location="Balaghat",
        crop="Soybean",
        growth_stage="Flowering",
        language="hi"
    )
    assert resp.language == "hi"
    assert "कृषिसार्थी" in resp.response
    assert len(resp.agent_traces) >= 5


# Scenario 14: Full bilingual chat English query execution
@pytest.mark.asyncio
async def test_scenario_14_english_chat():
    orch = KrishiOrchestrator()
    resp = await orch.execute_advisory_pipeline(
        query="Will heavy rain in Balaghat harm my flowering soybean?",
        location="Balaghat",
        crop="Soybean",
        growth_stage="Flowering",
        language="en"
    )
    assert resp.language == "en"
    assert "KrishiSathi Climate Intelligence Report" in resp.response
    assert len(resp.agent_traces) >= 5


# Scenario 15: Advisory 3-day action plan structure integrity
def test_scenario_15_advisory_3day_plan_integrity():
    w = build_scenario_weather("Balaghat", 28.0, 20.0, [35.0, 40.0, 5.0, 0.0, 0.0, 0.0, 0.0], [85, 80, 20, 10, 10, 10, 10])
    rep = DeterministicRiskEngine.calculate_risks(w, "Soybean", "Flowering")
    adv = client.post("/api/advisory/generate", json={
        "location": "Balaghat",
        "crop": "Soybean",
        "growth_stage": "Flowering",
        "language": "en"
    }).json()

    assert len(adv["action_plan_3d"]) == 3
    assert len(adv["immediate_precautions_en"]) > 0
    assert "official_advisory_note_en" in adv
