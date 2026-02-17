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
