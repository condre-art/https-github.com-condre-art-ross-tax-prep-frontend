from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

app = FastAPI(title="Tax Preparation API")


@app.get("/health")
def health_check():
    return {"status": "ok"}


class LicenseVerifyRequest(BaseModel):
    licenseId: str


class License(BaseModel):
    id: str
    status: str


@app.post("/api/licenses/verify", response_model=License)
def verify_license(payload: LicenseVerifyRequest):
    valid_license = os.getenv("VALID_LICENSE_ID", "valid-license")
    if payload.licenseId != valid_license:
        raise HTTPException(status_code=403, detail="License not valid")

    return License(id=payload.licenseId, status="verified")
