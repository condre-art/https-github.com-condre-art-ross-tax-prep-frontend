
from fastapi import APIRouter
from .workflows import on_new_credit_report, ai_generate_dispute_plan
from .lib.ews import run_ews_checks
from .lib.cade2 import run_cade2_checks

router = APIRouter()
@router.post("/pre_submission_check")
def pre_submission_check(data: dict):
    """
    Run EWS 2.0 and CADE2 pre-submission checks on provided data.
    Returns alerts and pass/fail for each system.
    """
    ews_result = run_ews_checks(data)
    cade2_result = run_cade2_checks(data)
    return {
        "EWS": ews_result,
        "CADE2": cade2_result,
        "all_passed": ews_result["passed"] and cade2_result["passed"]
    }

@router.post("/trigger/credit-report")
def trigger_credit_report(client_id: str, report_data: dict):
    return on_new_credit_report(client_id, report_data)

@router.post("/ai/dispute-plan")
def ai_dispute_plan(report_data: dict):
    return ai_generate_dispute_plan(report_data)
