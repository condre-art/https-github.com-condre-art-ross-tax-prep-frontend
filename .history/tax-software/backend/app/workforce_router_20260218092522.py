
from fastapi import APIRouter, Depends, HTTPException, status
from .blueprint import Employee, paestum, Timecard, Payroll, Onboarding, HRCase, ai_hr_director_advice, ai_human_rights_attorney
from typing import List
from datetime import datetime
import logging
from .auth_utils import bearer_auth, require_role

logger = logging.getLogger("tax-prep-app.workforce")

router = APIRouter()

# In-memory stores for demonstration (replace with DB in production)
employees = []
payouts = []
timecards = []
payrolls = []
onboardings = []
hrcases = []

# --- Employee Endpoints ---
@router.post("/employee", response_model=Employee)
def create_employee(emp: Employee, user = Depends(require_role(["admin", "staff"]))):
    employees.append(emp)
    logger.info(f"AUDIT: Employee created: {emp} by {user.email}")
    return emp

@router.get("/employee", response_model=List[Employee])
def list_employees():
    return employees

# --- Paystub Endpoints ---
@router.post("/payouts", response_model=Paystub)
def create_paystub(stub: Paystub, user = Depends(require_role(["admin", "staff"]))):
    paystubs.append(stub)
    logger.info(f"AUDIT: Paystub created: {stub} by {user.email}")
    return stub

@router.get("/paystub", response_model=List[Paystub])
def list_paystubs():
    return paystubs

# --- Timecard Endpoints ---
@router.post("/timecard", response_model=Timecard)
def create_timecard(tc: Timecard, user = Depends(require_role(["admin", "staff"]))):
    timecards.append(tc)
    logger.info(f"AUDIT: Timecard created: {tc} by {user.email}")
    return tc

@router.get("/timecard", response_model=List[Timecard])
def list_timecards():
    return timecards

# --- Payroll Endpoints ---
@router.post("/payroll", response_model=Payroll)
def create_payroll(pr: Payroll, user = Depends(require_role(["admin"]))):
    payrolls.append(pr)
    logger.info(f"AUDIT: Payroll created: {pr} by {user.email}")
    return pr

@router.get("/payroll", response_model=List[Payroll])
def list_payrolls():
    return payrolls

# --- Onboarding Endpoints ---
@router.post("/onboarding", response_model=Onboarding)
def create_onboarding(ob: Onboarding, token: str = Depends(bearer_auth)):
    onboardings.append(ob)
    logger.info(f"AUDIT: Onboarding created: {ob}")
    return ob

@router.get("/onboarding", response_model=List[Onboarding])
def list_onboardings():
    return onboardings

# --- HR Case Endpoints ---
@router.post("/hrcase", response_model=HRCase)
def create_hrcase(case: HRCase, token: str = Depends(bearer_auth)):
    hrcases.append(case)
    logger.info(f"AUDIT: HR case created: {case}")
    return case

@router.get("/hrcase", response_model=List[HRCase])
def list_hrcases():
    return hrcases

# --- AI Persona Endpoints ---
@router.post("/ai/hr-director-advice")
def hr_director_advice(emp: Employee, context: dict = {}, token: str = Depends(bearer_auth)):
    logger.info(f"AUDIT: HR director advice requested for {emp}")
    return ai_hr_director_advice(emp, context)

@router.post("/ai/human-rights-attorney")
def human_rights_attorney(emp: Employee, context: dict = {}, token: str = Depends(bearer_auth)):
    logger.info(f"AUDIT: Human rights attorney advice requested for {emp}")
    return ai_human_rights_attorney(emp, context)

# --- Auto-approval for all changes (demo) ---
@router.post("/autoapprove")
def autoapprove_all(token: str = Depends(bearer_auth)):
    logger.info("AUDIT: Autoapprove endpoint called")
    return {"autoapproval": True, "message": "All changes are auto-approved."}
