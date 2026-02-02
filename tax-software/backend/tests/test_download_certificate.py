from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_download_certificate_success():
    response = client.get(
        "/api/certificates/123/download",
        headers={"Authorization": "Bearer token"},
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.content.startswith(b"%PDF")


def test_download_certificate_unauthorized():
    response = client.get("/api/certificates/123/download")
    assert response.status_code == 401


def test_download_certificate_not_found():
    response = client.get(
        "/api/certificates/missing/download",
        headers={"Authorization": "Bearer token"},
    )
    assert response.status_code == 404
