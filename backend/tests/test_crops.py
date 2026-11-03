import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.tools.crop_tool import get_crop_profile, get_growth_stage_info, load_crop_knowledge


client = TestClient(app)


def test_load_crop_knowledge():
    data = load_crop_knowledge()
    assert "crops" in data
    assert "soybean" in data["crops"]
    assert "rice" in data["crops"]
    assert "wheat" in data["crops"]
    assert "maize" in data["crops"]
    assert "cotton" in data["crops"]


def test_get_crop_profile_soybean():
    profile = get_crop_profile("Soybean")
    assert profile["crop_name"] == "Soybean"
    assert profile["crop_name_hi"] == "सोयाबीन"
    assert len(profile["growth_stages"]) >= 5
    assert len(profile["sourced_references"]) > 0


def test_get_growth_stage_flowering():
    stage_info = get_growth_stage_info("Soybean", "Flowering")
    assert stage_info["crop"] == "Soybean"
    stage = stage_info["stage"]
    assert "Flowering" in stage["stage_name"]
    assert stage["temp_opt_max_c"] == 30.0
    assert "heat_stress" in stage["vulnerable_risks"]


def test_api_list_crops():
    response = client.get("/api/crops")
    assert response.status_code == 200
    crops = response.json()
    assert len(crops) >= 5
    names = [c["crop_name"] for c in crops]
    assert "Soybean" in names
    assert "Wheat" in names


def test_api_get_crop_details():
    response = client.get("/api/crops/wheat")
    assert response.status_code == 200
    data = response.json()
    assert data["crop_name"] == "Wheat"
    assert data["scientific_name"] == "Triticum aestivum"


def test_api_get_invalid_crop():
    response = client.get("/api/crops/unknown_crop_xyz")
    assert response.status_code == 404

