from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_current_license_requires_auth():
    response = client.get("/api/licenses/current")
    assert response.status_code == 401


def test_current_license_success():
    response = client.get(
        "/api/licenses/current", headers={"Authorization": "Bearer token"}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == "license-001"
    assert body["status"] == "active"
