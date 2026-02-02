from datetime import datetime
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

app = FastAPI(title="Tax Preparation API")


# -----------------------------
# Models
# -----------------------------
class Badge(BaseModel):
    id: int
    name: str
    description: str


class Certificate(BaseModel):
    id: int
    name: str
    issued_at: datetime
    expires_at: datetime


# -----------------------------
# Auth
# -----------------------------
def bearer_auth(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
) -> str:
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )
    return credentials.credentials


# -----------------------------
# Fake Data
# -----------------------------
FAKE_CERTIFICATES: List[Certificate] = [
    Certificate(
        id=1,
        name="Tenant Certificate 1",
        issued_at=datetime(2024, 1, 1),
        expires_at=datetime(2025, 1, 1),
    ),
    Certificate(
        id=2,
        name="Tenant Certificate 2",
        issued_at=datetime(2024, 6, 1),
        expires_at=datetime(2025, 6, 1),
    ),
]


# -----------------------------
# Health Check
# -----------------------------
@app.get("/health")
def health_check():
    return {"status": "ok"}


# -----------------------------
# Endpoints
# -----------------------------
@app.get(
    "/api/badges",
    response_model=List[Badge],
    tags=["Badges"],
    summary="List all badges for the current tenant",
)
def list_badges(_: str = Depends(bearer_auth)):
    return [
        Badge(id=1, name="Welcome Aboard", description="Completed profile setup"),
        Badge(id=2, name="Early Filer", description="Filed taxes before deadline"),
    ]


@app.get(
    "/api/certificates",
    response_model=List[Certificate],
    tags=["Certificates"],
    summary="List certificates for the current tenant",
)
def list_certificates(_: str = Depends(bearer_auth)):
    return FAKE_CERTIFICATES
