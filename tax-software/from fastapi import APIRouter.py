from fastapi import APIRouter
from .workflows import on_new_credit_report, ai_generate_dispute_plan

router = APIRouter()

@router.post("/trigger/credit-report")
def trigger_credit_report(client_id: str, report_data: dict):
    return on_new_credit_report(client_id, report_data)

@router.post("/ai/dispute-plan")
def ai_dispute_plan(report_data: dict):
    return ai_generate_dispute_plan(report_data)