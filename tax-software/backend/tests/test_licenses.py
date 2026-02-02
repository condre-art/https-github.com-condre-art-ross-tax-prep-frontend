from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_purchase_license_requires_auth_and_license_type():
    resp = client.post("/api/licenses/purchase", json={"licenseType": "affiliate"})
    assert resp.status_code == 401

    resp = client.post(
        "/api/licenses/purchase",
        json={"licenseType": "affiliate"},
        headers={"Authorization": "Bearer token"},
    )
    assert resp.status_code == 201
    assert resp.json()["licenseType"] == "affiliate"
    assert resp.json()["status"] == "pending"
