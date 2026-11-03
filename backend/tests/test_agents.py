import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.agents.orchestrator import KrishiOrchestrator
from app.agents.weather_agent import create_weather_agent
from app.agents.crop_agent import create_crop_agent
from app.agents.risk_agent import create_risk_agent
from app.agents.advisory_agent import create_advisory_agent

client = TestClient(app)


def test_specialist_agents_creation():
    w = create_weather_agent()
    c = create_crop_agent()
    r = create_risk_agent()
    a = create_advisory_agent()

    assert w.name == "WeatherIntelligenceAgent"
    assert c.name == "CropIntelligenceAgent"
    assert r.name == "RiskAssessmentAgent"
    assert a.name == "FarmingAdvisoryAgent"


def test_orchestrator_entity_extraction():
    orch = KrishiOrchestrator()
    
    # English query
    e1 = orch.extract_entities("I grow soybean in Balaghat. Heavy rainfall is predicted over the next two days.")
    assert e1["crop"] == "Soybean"
    assert e1["location"] == "Balaghat"
    assert e1["language"] == "en"

    # Hindi query
    e2 = orch.extract_entities("इंदौर में गेहूं की फसल में क्या आज सिंचाई करनी चाहिए?")
    assert e2["crop"] == "Wheat"
    assert e2["location"] == "Indore"
    assert e2["language"] == "hi"


@pytest.mark.asyncio
async def test_orchestrator_pipeline_english():
    orch = KrishiOrchestrator()
    res = await orch.execute_advisory_pipeline(
        query="I grow soybean in Balaghat. Heavy rainfall is predicted over the next two days. What should I do?",
        location="Balaghat",
        crop="Soybean",
        growth_stage="Flowering",
        language="en"
    )

    assert res.language == "en"
    assert "KrishiSathi Climate Intelligence Report" in res.response
    assert len(res.agent_traces) >= 5

    # Check agent trace steps
    agent_names = [t.agent for t in res.agent_traces]
    assert "KrishiOrchestrator" in agent_names
    assert "WeatherIntelligenceAgent" in agent_names
    assert "CropIntelligenceAgent" in agent_names
    assert "RiskAssessmentAgent" in agent_names
    assert "FarmingAdvisoryAgent" in agent_names


@pytest.mark.asyncio
async def test_orchestrator_pipeline_hindi():
    orch = KrishiOrchestrator()
    res = await orch.execute_advisory_pipeline(
        query="बालाघाट में सोयाबीन में फूल आ रहे हैं, भारी बारिश होने वाली है, क्या करें?",
        location="Balaghat",
        crop="Soybean",
        growth_stage="Flowering",
        language="hi"
    )

    assert res.language == "hi"
    assert "कृषिसार्थी कृषि जलवायु रिपोर्ट" in res.response
    assert "सावधानियां" in res.response
    assert len(res.agent_traces) >= 5


def test_api_chat_endpoint():
    payload = {
        "query": "Will rainfall damage my soybean crop in Balaghat?",
        "location": "Balaghat",
        "crop": "Soybean",
        "growth_stage": "Flowering",
        "language": "en"
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "agent_traces" in data
    assert len(data["agent_traces"]) >= 5
    assert data["extracted_entities"]["crop"] == "Soybean"


def test_api_advisory_generate_endpoint():
    payload = {
        "location": "Balaghat",
        "crop": "Soybean",
        "growth_stage": "Flowering",
        "language": "en"
    }
    response = client.post("/api/advisory/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["crop"] == "Soybean"
    assert "immediate_precautions_en" in data
    assert len(data["action_plan_3d"]) == 3

