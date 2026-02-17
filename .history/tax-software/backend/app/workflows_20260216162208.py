from fastapi import APIRouter

def on_new_credit_report(client_id: str, report_data: dict):
    # AI workflow logic stub
    return {"message": f"Workflow triggered for client {client_id}", "plan": ai_generate_dispute_plan(report_data)}

def ai_generate_dispute_plan(report_data: dict):
    # AI persona stub logic
    return {"steps": ["Dispute late payment", "Request validation"]}
