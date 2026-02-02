import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client():
    return TestClient(app)


def test_badges_requires_auth(client):
    resp = client.get("/api/badges")
    assert resp.status_code == 401


def test_badges_returns_list(client):
    resp = client.get("/api/badges", headers={"Authorization": "Bearer token"})
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    first = data[0]
    assert {"id", "name", "description"} <= set(first.keys())
