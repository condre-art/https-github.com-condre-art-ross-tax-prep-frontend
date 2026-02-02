from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from typing import List

from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

app = FastAPI(title="Tax Preparation API")


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


class LicenseRequest(BaseModel):
    licenseType: str = Field(..., pattern="^(affiliate|reseller|enterprise)$")
    seats: Optional[int] = Field(default=None, ge=1)


class License(BaseModel):
    id: int
    licenseType: str
    seats: Optional[int] = None
    status: str


@app.post("/api/licenses/purchase", status_code=status.HTTP_201_CREATED, response_model=License, tags=["Licenses"])
def purchase_license(payload: LicenseRequest, authorization: Optional[str] = Header(default=None, convert_underscores=False)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    return License(
        id=1,
        licenseType=payload.licenseType,
        seats=payload.seats,
        status="pending",
    )
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
