
from fastapi import APIRouter, Depends, HTTPException, status
from .blueprint import Employee, Paystub, Timecard, Payroll, Onboarding, HRCase, ai_hr_director_advice, ai_human_rights_attorney
from typing import List
from datetime import datetime
import logging

from .auth_utils import bearer_auth, require_role
from .db import SessionLocal, EmployeeORM, PaystubORM, TimecardORM, PayrollORM, OnboardingORM, HRCaseORM
from .lib.cade2 import run_cade2_checks
from .lib.ews import run_ews_checks
from fastapi import Depends
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

logger = logging.getLogger("tax-prep-app.workforce")

router = APIRouter()



# --- Employee Endpoints ---

@router.post("/employee", response_model=Employee)
def create_employee(emp: Employee, user = Depends(require_role(["admin", "staff"])), db: Session = Depends(get_db)):
    db_emp = EmployeeORM(**emp.dict())
    db.add(db_emp)
    db.commit()
    db.refresh(db_emp)
    logger.info(f"AUDIT: Employee created: {emp} by {user.email}")
    return emp


@router.get("/employee", response_model=List[Employee])
def list_employees(db: Session = Depends(get_db)):
    return db.query(EmployeeORM).all()

# --- Paystub Endpoints ---

@router.post("/payouts", response_model=Paystub)
def create_paystub(stub: Paystub, user = Depends(require_role(["admin", "staff"])), db: Session = Depends(get_db)):
    # Run compliance checks
    cade2_result = run_cade2_checks(stub.dict())
    ews_result = run_ews_checks(stub.dict())
    logger.info(f"COMPLIANCE: CADE2 result: {cade2_result}")
    logger.info(f"COMPLIANCE: EWS result: {ews_result}")
    if not cade2_result["passed"] or not ews_result["passed"]:
        logger.warning(f"COMPLIANCE ALERT: {cade2_result['alerts'] + ews_result['alerts']}")
        return {"status": "error", "alerts": cade2_result["alerts"] + ews_result["alerts"]}
    db_stub = PaystubORM(**stub.dict())
    db.add(db_stub)
    db.commit()
    db.refresh(db_stub)
    logger.info(f"AUDIT: Paystub created: {stub} by {user.email}")
    return stub


@router.get("/paystub", response_model=List[Paystub])
def list_paystubs(db: Session = Depends(get_db)):
    return db.query(PaystubORM).all()

# --- Timecard Endpoints ---

@router.post("/timecard", response_model=Timecard)
def create_timecard(tc: Timecard, user = Depends(require_role(["admin", "staff"])), db: Session = Depends(get_db)):
    db_tc = TimecardORM(**tc.dict())
    db.add(db_tc)
    db.commit()
    db.refresh(db_tc)
    logger.info(f"AUDIT: Timecard created: {tc} by {user.email}")
    return tc


@router.get("/timecard", response_model=List[Timecard])
def list_timecards(db: Session = Depends(get_db)):
    return db.query(TimecardORM).all()

# --- Payroll Endpoints ---

@router.post("/payroll", response_model=Payroll)
def create_payroll(pr: Payroll, user = Depends(require_role(["admin"])), db: Session = Depends(get_db)):
    db_pr = PayrollORM(**pr.dict(exclude={"paystubs"}))
    db.add(db_pr)
    db.commit()
    db.refresh(db_pr)
    logger.info(f"AUDIT: Payroll created: {pr} by {user.email}")
    return pr


@router.get("/payroll", response_model=List[Payroll])
def list_payrolls(db: Session = Depends(get_db)):
    return db.query(PayrollORM).all()

# --- Onboarding Endpoints ---

@router.post("/onboarding", response_model=Onboarding)
def create_onboarding(ob: Onboarding, token: str = Depends(bearer_auth), db: Session = Depends(get_db)):
    db_ob = OnboardingORM(**ob.dict())
    db.add(db_ob)
    db.commit()
    db.refresh(db_ob)
    logger.info(f"AUDIT: Onboarding created: {ob}")
    return ob


@router.get("/onboarding", response_model=List[Onboarding])
def list_onboardings(db: Session = Depends(get_db)):
    return db.query(OnboardingORM).all()

# --- HR Case Endpoints ---

@router.post("/hrcase", response_model=HRCase)
def create_hrcase(case: HRCase, token: str = Depends(bearer_auth), db: Session = Depends(get_db)):
    db_case = HRCaseORM(**case.dict())
    db.add(db_case)
    db.commit()
    db.refresh(db_case)
    logger.info(f"AUDIT: HR case created: {case}")
    return case


@router.get("/hrcase", response_model=List[HRCase])
def list_hrcases(db: Session = Depends(get_db)):
    return db.query(HRCaseORM).all()

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
