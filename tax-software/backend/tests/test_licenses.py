from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_verify_license_success():
    payload = {"licenseId": "valid-license"}
    response = client.post("/api/licenses/verify", json=payload)

    assert response.status_code == 200
    assert response.json() == {"id": "valid-license", "status": "verified"}


def test_verify_license_requires_license_id():
    response = client.post("/api/licenses/verify", json={})
    assert response.status_code == 422


def test_verify_license_rejects_invalid():
    payload = {"licenseId": "invalid"}
    response = client.post("/api/licenses/verify", json=payload)

    assert response.status_code == 403
