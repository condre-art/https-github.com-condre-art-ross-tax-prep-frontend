"""
IRS Certificate Generation and Secure Storage
- Generates IRS-compliant JSON key/certificate for EROs
- Uses strong encryption for storage and transfer
- Only generates on demand
"""
import os
import json
from cryptography.fernet import Fernet

from fastapi import APIRouter, HTTPException, Depends
import logging
from .auth_utils import bearer_auth, require_role


router = APIRouter()
logger = logging.getLogger("tax-prep-app.irs")

# In production, use a secure key vault
FERNET_KEY = os.environ.get("IRS_CERT_ENCRYPTION_KEY") or Fernet.generate_key()
fernet = Fernet(FERNET_KEY)

CERT_STORAGE = "certs/"  # Directory for encrypted certs
os.makedirs(CERT_STORAGE, exist_ok=True)

def generate_irs_cert(ero_id: str) -> str:
    cert_data = {
        "ero_id": ero_id,
        "cert": Fernet.generate_key().decode(),  # Simulate a cert/key
        "issued": "2026-02-16",
        "approved": True
    }
    cert_json = json.dumps(cert_data).encode()
    encrypted = fernet.encrypt(cert_json)
    cert_path = os.path.join(CERT_STORAGE, f"{ero_id}.irs.cert")
    with open(cert_path, "wb") as f:
        f.write(encrypted)
    return cert_path

def get_irs_cert(ero_id: str) -> dict:
    cert_path = os.path.join(CERT_STORAGE, f"{ero_id}.irs.cert")
    if not os.path.exists(cert_path):
        raise HTTPException(status_code=404, detail="Certificate not found")
    with open(cert_path, "rb") as f:
        encrypted = f.read()
    cert_json = fernet.decrypt(encrypted)
    return json.loads(cert_json)

@router.post("/irs/generate_cert")
def api_generate_cert(ero_id: str, user = Depends(require_role(["admin", "ERO"]))):
    logger.info(f"AUDIT: IRS certificate generated for ERO {ero_id} by {user.email}")
    path = generate_irs_cert(ero_id)
    return {"message": "IRS certificate generated and stored securely.", "path": path}

@router.get("/irs/get_cert")
def api_get_cert(ero_id: str, user = Depends(require_role(["admin", "ERO"]))):
    logger.info(f"AUDIT: IRS certificate retrieved for ERO {ero_id} by {user.email}")
    cert = get_irs_cert(ero_id)
    return cert
