
from fastapi import APIRouter
from .workflows import on_new_credit_report, ai_generate_dispute_plan
from .lib.ews import run_ews_checks
from .lib.cade2 import run_cade2_checks
from .blueprint import User

router = APIRouter()

def ai_risk_score(data: dict) -> dict:
    # Heavy AI risk scoring stub (expand with real model)
    score = 0
    reasons = []
    if data.get("refund_amount", 0) > 15000:
        score += 40
        reasons.append("High refund amount")
    if data.get("ssn") in {"123-45-6789", "987-65-4321"}:
        score += 30
        reasons.append("Blacklisted SSN")
    if data.get("user_id") in {"user123", "user456"}:
        score += 20
        reasons.append("Duplicate filer")
    # Add more AI/ML features here
    return {"score": score, "reasons": reasons, "risk_level": "high" if score > 50 else "medium" if score > 20 else "low"}

def ai_assist_validation(data: dict) -> dict:
    # AI assistive validation stub
    suggestions = []
    if not data.get("w2_attached"):
        suggestions.append("Attach W-2 for income validation")
    if not data.get("id_verified"):
        suggestions.append("Complete ID verification")
    # Add more validation logic as needed
    return {"suggestions": suggestions, "all_valid": not suggestions}

@router.post("/pre_submission_check")
def pre_submission_check(data: dict):
    """
    Run EWS 2.0, CADE2, AI risk scoring, and assistive validation checks on provided data.
    Returns alerts, risk score, validation suggestions, and pass/fail for each system.
    """
    ews_result = run_ews_checks(data)
    cade2_result = run_cade2_checks(data)
    risk_result = ai_risk_score(data)
    assist_result = ai_assist_validation(data)
    return {
        "EWS": ews_result,
        "CADE2": cade2_result,
        "AI_RiskScore": risk_result,
        "AI_AssistValidation": assist_result,
        "all_passed": ews_result["passed"] and cade2_result["passed"] and assist_result["all_valid"]
    }

@router.post("/trigger/credit-report")
def trigger_credit_report(client_id: str, report_data: dict):
    return on_new_credit_report(client_id, report_data)

@router.post("/ai/dispute-plan")
def ai_dispute_plan(report_data: dict):
    return ai_generate_dispute_plan(report_data)
