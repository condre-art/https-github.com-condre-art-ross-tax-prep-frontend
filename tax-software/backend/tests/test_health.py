from fastapi.testclient import TestClient

from app.main import app
from app.main import FAKE_CERTIFICATES

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_certificates():
    response = client.get("/api/certificates")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == len(FAKE_CERTIFICATES)
    for idx, cert in enumerate(data):
        assert cert["id"] == FAKE_CERTIFICATES[idx].id
        assert cert["name"] == FAKE_CERTIFICATES[idx].name
