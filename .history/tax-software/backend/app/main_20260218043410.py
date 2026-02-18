# --- IRS E-file ETIN Transmission Endpoint (Stub) ---
@app.post("/api/irs/send-etin-files", tags=["IRS"])
def send_files_to_irs_etin(data: dict, token: str = Depends(bearer_auth)):
    etin = data.get("etin")
    mode = data.get("mode", "production")  # 'production' or 'test'
    # Simulate sending files to IRS.gov for the given ETIN and mode
    # In production, integrate with IRS e-file system
    if not etin:
        return {"status": "error", "message": "ETIN required"}
    if mode not in ("production", "test"):
        return {"status": "error", "message": "Mode must be 'production' or 'test'"}
    # Simulate a successful transmission
    return {"status": "success", "message": f"Files sent to IRS.gov for ETIN {etin} in {mode} mode"}
# --- IRS E-file Test Transmission Endpoint (Stub) ---
@app.post("/api/irs/send-test-files", tags=["IRS"])
def send_test_files_to_irs(data: dict, token: str = Depends(bearer_auth)):
    efin = data.get("efin")
    # Simulate sending test files to IRS.gov for the given EFIN
    # In production, integrate with IRS e-file system
    if not efin:
        return {"status": "error", "message": "EFIN required"}
    # Simulate a successful transmission
    return {"status": "success", "message": f"Test files sent to IRS.gov for EFIN {efin}"}
# --- E-file Transmission Kill Switch ---
EFILE_KILL_SWITCH = {"enabled": True}

@app.get("/api/efile/kill-switch", tags=["Efile"])
def get_efile_kill_switch(token: str = Depends(bearer_auth)):
    return {"enabled": EFILE_KILL_SWITCH["enabled"]}

@app.post("/api/efile/kill-switch", tags=["Efile"])
def set_efile_kill_switch(data: dict, token: str = Depends(bearer_auth)):
    EFILE_KILL_SWITCH["enabled"] = bool(data.get("enabled", True))
    return {"enabled": EFILE_KILL_SWITCH["enabled"]}
from agent_framework.observability import configure_otel_providers
import logging

configure_otel_providers(
    vs_code_extension_port=4317,  # AI Toolkit gRPC port
    enable_sensitive_data=True  # Enable capturing prompts and completions
)

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("tax-prep-app")
from datetime import datetime
from typing import List

from fastapi import Depends, FastAPI, Header, HTTPException, status
from .workflow_router import router as workflow_router
from .admin_router import router as admin_router
from .workforce_router import router as workforce_router
from .irs_router import router as irs_router
from .xml_router import router as xml_router
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel


app = FastAPI(title="Tax Preparation API")
app.include_router(workflow_router, prefix="/api/workflow", tags=["Workflow"])
app.include_router(admin_router, prefix="/api/admin", tags=["Admin"])
app.include_router(workforce_router, prefix="/api/workforce", tags=["Workforce", "HR", "Payroll", "WhiteLabel"])
app.include_router(irs_router, prefix="/api", tags=["IRS", "Certificates"])
app.include_router(xml_router, prefix="/api", tags=["XML", "ExpertXML"])


class Badge(BaseModel):
    id: int
    name: str
    description: str


class Certificate(BaseModel):
    id: int
    name: str
    issued_at: datetime
    expires_at: datetime



# --- Auth & RBAC Utilities ---
def bearer_auth(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
) -> str:
    if not credentials or not credentials.scheme.lower() == "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    return credentials.credentials

def get_user_from_token(token: str):
    # TODO: Replace with real JWT decode/validation
    # For demo, return a fake user based on token value
    # e.g., token == "admin" => admin user
    from .blueprint import User
    if token == "admin":
        return User(id=1, email="admin@example.com", name="Admin", role="admin", tenant_id="t1")
    if token == "staff":
        return User(id=2, email="staff@example.com", name="Staff", role="staff", tenant_id="t1")
    if token == "client":
        return User(id=3, email="client@example.com", name="Client", role="client", tenant_id="t1")
    return User(id=0, email="anon@example.com", name="Anon", role="anon", tenant_id="t1")

def require_role(required_roles):
    def role_dependency(token: str = Depends(bearer_auth)):
        user = get_user_from_token(token)
        if user.role not in required_roles and "*" not in required_roles:
            raise HTTPException(status_code=403, detail="Insufficient role")
        return user
    return role_dependency


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


# --- Custom API Endpoints for Widgets ---
from fastapi import Request

# In-memory demo stores (replace with DB in production)
NOTIFICATIONS = [
    {"id": 1, "title": "Welcome!", "body": "Your account is ready.", "time": "2024-06-01T10:00:00Z", "read": False},
    {"id": 2, "title": "Tax Deadline", "body": "File by April 15.", "time": "2024-06-02T12:00:00Z", "read": False},
]
AUDIT_LOG = [
    {"time": "2024-06-01T09:00:00Z", "user": "admin@example.com", "action": "Login", "details": "Admin logged in."},
    {"time": "2024-06-01T10:05:00Z", "user": "client@example.com", "action": "Profile Update", "details": "Client updated address."},
]
CHAT_MESSAGES = [
    {"from": "Staff", "text": "Welcome! How can we help you today?", "time": "2024-06-01T08:00:00Z"},
]
EXPECTED_REFUND = {"refundAmount": 1234.56, "status": "Pending", "lastUpdated": "2024-06-01T11:00:00Z"}


@app.get("/api/notifications", tags=["Notifications"])
def get_notifications(token: str = Depends(bearer_auth)):
    # In production, filter by user/tenant
    return NOTIFICATIONS

@app.post("/api/notifications/mark-read", tags=["Notifications"])
def mark_notification_read(id: int, token: str = Depends(bearer_auth)):
    for n in NOTIFICATIONS:
        if n["id"] == id:
            n["read"] = True
    return {"status": "ok"}

@app.get("/api/audit-log", tags=["AuditLog"])
def get_audit_log(token: str = Depends(bearer_auth)):
    return AUDIT_LOG

@app.get("/api/chat", tags=["Chat"])
def get_chat_messages(token: str = Depends(bearer_auth)):
    return CHAT_MESSAGES

@app.post("/api/chat", tags=["Chat"])
def post_chat_message(msg: dict, token: str = Depends(bearer_auth)):
    # msg: {"from": "You", "text": "..."}
    from datetime import datetime
    msg["time"] = datetime.utcnow().isoformat() + "Z"
    CHAT_MESSAGES.append(msg)
    return {"status": "sent"}

@app.get("/api/expected-refund", tags=["Refund"])
def get_expected_refund(token: str = Depends(bearer_auth)):
    return EXPECTED_REFUND
