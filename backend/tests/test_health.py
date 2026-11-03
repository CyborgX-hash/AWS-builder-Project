import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.session import init_db


@pytest.fixture(autouse=True)
def setup_database():
    """Ensure database tables are initialized before tests."""
    init_db()


def test_root_endpoint():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["project"] == "KrishiSathi"
        assert data["status"] == "online"


def test_health_endpoint():
    with TestClient(app) as client:
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "KrishiSathi"
        assert "timestamp" in data


def test_create_farmer_profile():
    with TestClient(app) as client:
        payload = {
            "name": "Ramesh Patel",
            "preferred_language": "hi",
            "location": "Balaghat, Madhya Pradesh",
            "latitude": 21.8129,
            "longitude": 80.1838,
            "crop_name": "Soybean",
            "growth_stage": "Flowering"
        }
        response = client.post("/api/farmer/profile", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Ramesh Patel"
        assert data["location"] == "Balaghat, Madhya Pradesh"
        assert data["preferred_language"] == "hi"
        assert "id" in data
