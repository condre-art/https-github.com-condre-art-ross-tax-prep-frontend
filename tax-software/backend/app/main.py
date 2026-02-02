from fastapi import FastAPI, Header, HTTPException, Response
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


@app.get(
    "/api/certificates/{certificateId}/download",
    response_class=Response,
    responses={
        200: {"content": {"application/pdf": {}}},
        401: {"description": "Unauthorized"},
        404: {"description": "Not found"},
    },
)
def download_certificate(certificateId: str, authorization: str | None = Header(default=None)):
    if authorization is None or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")

    if certificateId == "missing":
        raise HTTPException(status_code=404, detail="Not found")

    pdf_bytes = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog >>\nendobj\ntrailer\n<<>>\n%%EOF"
    return Response(content=pdf_bytes, media_type="application/pdf")
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
