from fastapi import APIRouter
from .blueprint import Employee, Paystub, Timecard, Payroll, Onboarding, HRCase, ai_hr_director_advice, ai_human_rights_attorney
from typing import List
from datetime import datetime

router = APIRouter()

# In-memory stores for demonstration (replace with DB in production)
employees = []
paystubs = []
timecards = []
payrolls = []
onboardings = []
hrcases = []

# --- Employee Endpoints ---
@router.post("/employee", response_model=Employee)
def create_employee(emp: Employee):
    employees.append(emp)
    return emp

@router.get("/employee", response_model=List[Employee])
def list_employees():
    return employees

# --- Paystub Endpoints ---
@router.post("/paystub", response_model=Paystub)
def create_paystub(stub: Paystub):
    paystubs.append(stub)
    return stub

@router.get("/paystub", response_model=List[Paystub])
def list_paystubs():
    return paystubs

# --- Timecard Endpoints ---
@router.post("/timecard", response_model=Timecard)
def create_timecard(tc: Timecard):
    timecards.append(tc)
    return tc

@router.get("/timecard", response_model=List[Timecard])
def list_timecards():
    return timecards

# --- Payroll Endpoints ---
@router.post("/payroll", response_model=Payroll)
def create_payroll(pr: Payroll):
    payrolls.append(pr)
    return pr

@router.get("/payroll", response_model=List[Payroll])
def list_payrolls():
    return payrolls

# --- Onboarding Endpoints ---
@router.post("/onboarding", response_model=Onboarding)
def create_onboarding(ob: Onboarding):
    onboardings.append(ob)
    return ob

@router.get("/onboarding", response_model=List[Onboarding])
def list_onboardings():
    return onboardings

# --- HR Case Endpoints ---
@router.post("/hrcase", response_model=HRCase)
def create_hrcase(case: HRCase):
    hrcases.append(case)
    return case

@router.get("/hrcase", response_model=List[HRCase])
def list_hrcases():
    return hrcases

# --- AI Persona Endpoints ---
@router.post("/ai/hr-director-advice")
def hr_director_advice(emp: Employee, context: dict = {}):
    return ai_hr_director_advice(emp, context)

@router.post("/ai/human-rights-attorney")
def human_rights_attorney(emp: Employee, context: dict = {}):
    return ai_human_rights_attorney(emp, context)

# --- Auto-approval for all changes (demo) ---
@router.post("/autoapprove")
def autoapprove_all():
    return {"autoapproval": True, "message": "All changes are auto-approved."}
