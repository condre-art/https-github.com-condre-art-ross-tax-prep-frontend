from datetime import datetime
from typing import List

from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

app = FastAPI(title="Tax Preparation API")

security = HTTPBearer(auto_error=False)


class License(BaseModel):
    id: str
    status: str
    issued_at: date
    expires_at: date


def require_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> None:
    if (
        credentials is None
        or not credentials.credentials
        or credentials.scheme.lower() != "bearer"
    ):
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.get("/api/licenses/current", response_model=License, tags=["Licenses"])
def get_current_license(_: None = Depends(require_token)) -> License:
    return License(
        id="license-001",
        status="active",
        issued_at=date(2024, 1, 1),
        expires_at=date(2099, 12, 31),
    )


class Badge(BaseModel):
    id: int
    name: str
    description: str


class Certificate(BaseModel):
    id: int
    name: str
    issued_at: datetime
    expires_at: datetime


def bearer_auth(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
) -> str:
    if not credentials or not credentials.scheme.lower() == "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    return credentials.credentials


@app.get("/health")
def health_check():
    return {"status": "ok"}


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


@app.get(
    "/api/badges",
    response_model=list[Badge],
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
