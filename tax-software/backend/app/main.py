from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(title="Tax Preparation API")


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
