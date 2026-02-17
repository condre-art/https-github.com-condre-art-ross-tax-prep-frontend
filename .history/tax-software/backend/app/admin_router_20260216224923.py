
from fastapi import APIRouter, HTTPException, status, Depends
from .blueprint import User, Role, PermissionChangeRequest, TenantConfig, evaluate_tax_rules, auto_generate_tax_plan, auto_credit_dispute
import logging
logger = logging.getLogger("tax-prep-app.admin")

router = APIRouter()

# In-memory stores for demo (replace with DB in production)
USERS = [User(id=1, email="admin@example.com", name="Admin", role="admin", tenant_id="t1")]
ROLES = [Role(id=1, name="admin", permissions=["all"]), Role(id=2, name="client", permissions=["view", "submit"])]
TENANT_CONFIGS = [TenantConfig(tenant_id="t1", brand_name="Acme Tax", theme="ios", features=["payroll", "credit"]) ]

# Role/Permission Endpoints
@router.get("/users", response_model=list[User])
def list_users():
    return USERS

@router.post("/users/role-change")
def change_user_role(req: PermissionChangeRequest):
    user = next((u for u in USERS if u.id == req.user_id), None)
    if not user:
        logger.warning(f"Role change failed: user {req.user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    if req.admin_override or user.role == "admin":
        old_role = user.role
        user.role = req.new_role
        logger.info(f"AUDIT: Role changed for user {user.id} from {old_role} to {user.role} by admin_override={req.admin_override}")
        return {"status": "Role updated", "user": user}
    logger.warning(f"Role change denied for user {user.id}: admin override required")
    raise HTTPException(status_code=403, detail="Admin override required")

# White-labeling
@router.get("/tenant/config", response_model=list[TenantConfig])
def get_tenant_configs():
    return TENANT_CONFIGS

# Automation/AI Endpoints
@router.post("/ai/tax-plan")
def ai_tax_plan(user: User, data: dict):
    return auto_generate_tax_plan(user, data)

@router.post("/ai/credit-dispute")
def ai_credit_dispute(user: User, report: dict):
    return auto_credit_dispute(user, report)

# Tax Law Rule Engine
@router.post("/tax/rules/evaluate")
def tax_rule_evaluate(user: User, data: dict):
    return evaluate_tax_rules(user, data)
