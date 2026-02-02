from datetime import date

from fastapi import Depends, FastAPI, HTTPException
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


@app.get("/health")
def health_check():
    return {"status": "ok"}
