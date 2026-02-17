"""
Blueprint: Advanced Backend Architecture
- Modular: users, roles, permissions, tenants, workflows, automation, AI, white-label
- Extensible: add new rules, workflows, or AI personas easily
- Secure: admin override, audit logging, role-based access
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

# User, Role, Permission Models

# --- Roles ---
class Role(BaseModel):
    id: int
    name: str  # e.g., admin, staff, client, ERO
    permissions: List[str]

# Predefined roles
ROLES = [
    Role(id=1, name="admin", permissions=["*"]),
    Role(id=2, name="ERO", permissions=["start_return", "approve_return", "view_clients"]),
    Role(id=3, name="client", permissions=["start_return", "view_own"]),
    Role(id=4, name="staff", permissions=["view_clients", "assist_return"]),
]


# --- User Model with password hash and encrypted fields ---
class User(BaseModel):
    id: int
    email: str
    name: str
    role: str
    tenant_id: Optional[str]
    status: str = "active"
    password_hash: Optional[str] = None  # store hashed password
    encrypted_ssn: Optional[str] = None  # example of encrypted sensitive info

class PermissionChangeRequest(BaseModel):
    user_id: int
    new_role: str
    admin_override: bool = False

# White-labeling
class TenantConfig(BaseModel):
    tenant_id: str
    brand_name: str
    theme: str
    features: List[str]


# Workforce/HR/Tax Models
class Employee(BaseModel):
    id: int
    name: str
    email: str
    tenant_id: str
    status: str = "active"
    hire_date: Optional[datetime]
    role: str

class Paystub(BaseModel):
    id: int
    employee_id: int
    period_start: datetime
    period_end: datetime
    gross_pay: float
    net_pay: float
    taxes_withheld: float
    tenant_id: str

class Timecard(BaseModel):
    id: int
    employee_id: int
    date: datetime
    hours_worked: float
    approved: bool = False
    tenant_id: str

class Payroll(BaseModel):
    id: int
    run_date: datetime
    total_gross: float
    total_net: float
    tenant_id: str
    paystubs: List[Paystub]

class Onboarding(BaseModel):
    id: int
    employee_id: int
    start_date: datetime
    completed: bool = False
    tenant_id: str

class HRCase(BaseModel):
    id: int
    employee_id: int
    opened: datetime
    closed: Optional[datetime]
    case_type: str
    description: str
    status: str = "open"
    tenant_id: str

# AI Persona Stubs
def ai_hr_director_advice(employee: Employee, context: dict) -> dict:
    # AI persona: HR Director guidance
    return {"advice": ["Ensure onboarding compliance", "Review timecard approvals"]}

def ai_human_rights_attorney(employee: Employee, context: dict) -> dict:
    # AI persona: Human Rights Attorney guidance
    return {"advice": ["Verify anti-discrimination policies", "Audit payroll for wage compliance"]}

# Tax Law Rule Engine (Stub)
def evaluate_tax_rules(user: User, data: dict) -> dict:
    # Example: check for EITC eligibility
    result = {}
    if data.get("income", 0) < 60000 and user.role == "client":
        result["EITC_eligible"] = True
    # Add more rules as needed
    return result

# Automation/AI Workflow Stubs
def auto_generate_tax_plan(user: User, data: dict) -> dict:
    # AI persona stub: suggest deductions, credits, etc.
    return {"plan": ["Maximize EITC", "Deduct home office"]}

def auto_credit_dispute(user: User, report: dict) -> dict:
    # AI persona stub: generate dispute letters
    return {"letters": ["Dispute late payment", "Request validation"]}
