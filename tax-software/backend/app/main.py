from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Tax Preparation API")


class Certificate(BaseModel):
    id: int
    name: str
    issued_at: datetime
    expires_at: datetime


FAKE_CERTIFICATES = [
    Certificate(
        id=1,
        name="Tenant Certificate 1",
        issued_at=datetime(2024, 1, 1, 0, 0, 0),
        expires_at=datetime(2025, 1, 1, 0, 0, 0),
    ),
    Certificate(
        id=2,
        name="Tenant Certificate 2",
        issued_at=datetime(2024, 6, 1, 0, 0, 0),
        expires_at=datetime(2025, 6, 1, 0, 0, 0),
    ),
]


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/api/certificates", response_model=list[Certificate])
def list_certificates():
    return FAKE_CERTIFICATES
