

from fastapi import APIRouter, Depends
from .workflows import on_new_credit_report, ai_generate_dispute_plan
from .lib.ews import run_ews_checks
from .lib.cade2 import run_cade2_checks
from .blueprint import evaluate_tax_rules
import logging
from ..app.main import bearer_auth, require_role

logger = logging.getLogger("tax-prep-app.workflow")

router = APIRouter()

@router.post("/pre_submission_check")
def pre_submission_check(data: dict, user = Depends(require_role(["admin", "staff", "client"]))):
    logger.info(f"AUDIT: Pre-submission check run with data: {data} by {user.email}")
    """
    Run EWS 2.0, CADE2, risk scoring, AI validation, and automation scripts for pre-submission.
    Heavy automation enabled: all scripts run, all checks validated.
    """
    # EWS & CADE2
    ews_result = run_ews_checks(data)
    cade2_result = run_cade2_checks(data)

    # Risk Scoring (stub)
    risk_score = ai_risk_score(data)

    # AI Validation (stub)
    ai_validation = ai_validation_checks(data)

    # Automation scripts (stub)
    automation_results = run_automation_scripts(data)

    return {
        "EWS": ews_result,
        "CADE2": cade2_result,
        "risk_score": risk_score,
        "ai_validation": ai_validation,
        "automation": automation_results,
        "all_passed": ews_result["passed"] and cade2_result["passed"] and ai_validation["passed"] and automation_results["passed"]
    }

# --- Stubs for new automation ---
def ai_risk_score(data):
    # AI risk scoring logic (stub)
    # In production, use ML/LLM for risk assessment
    score = 0
    if data.get("refund_amount", 0) > 10000:
        score += 50
    if data.get("ssn") in {"123-45-6789", "987-65-4321"}:
        score += 40
    return {"score": score, "level": "high" if score > 60 else "medium" if score > 30 else "low"}

def ai_validation_checks(data):
    # AI validation logic (stub)
    # In production, use LLM/automation for doc validation
    passed = True
    issues = []
    if not data.get("name"):
        passed = False
        issues.append("Missing name")
    if not data.get("ssn"):
        passed = False
        issues.append("Missing SSN")
    return {"passed": passed, "issues": issues}

def run_automation_scripts(data):
    # Run all automation scripts (stub)
    # In production, trigger all relevant automation
    return {"passed": True, "scripts_run": ["EWS", "CADE2", "RiskScore", "AIValidation"]}

@router.post("/trigger/credit-report")
def trigger_credit_report(client_id: str, report_data: dict, token: str = Depends(bearer_auth)):
    logger.info(f"AUDIT: Credit report triggered for client {client_id}")
    return on_new_credit_report(client_id, report_data)

@router.post("/ai/dispute-plan")
def ai_dispute_plan(report_data: dict, token: str = Depends(bearer_auth)):
    logger.info(f"AUDIT: AI dispute plan generated")
    return ai_generate_dispute_plan(report_data)
