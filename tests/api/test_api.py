from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Enterprise Product Analytics Intelligence Platform"
    assert data["status"] == "running"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "enterprise-product-analytics"


def test_docs():
    response = client.get("/docs")

    assert response.status_code == 200
