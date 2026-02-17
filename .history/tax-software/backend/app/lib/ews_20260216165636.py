"""
EWS 2.0 (Early Warning System) logic for pre-submission checks.
This module provides real-time fraud, compliance, and data integrity checks.
"""

from typing import Dict, Any


# Example rules (expand as needed)
EWS_RULES = [
    ("SSN Blacklist", lambda data: data.get("ssn") in {"123-45-6789", "987-65-4321"}),
    ("High Refund Alert", lambda data: data.get("refund_amount", 0) > 10000),
    ("Duplicate Filing", lambda data: data.get("user_id") in get_recent_filers()),
    ("CC Check Failed", lambda data: not cc_check(data.get("cc_number"))),
    ("AI Validation Failed", lambda data: not ai_validation(data)),
]

def cc_check(cc_number):
    # Placeholder: Luhn algorithm or external service
    if not cc_number or not isinstance(cc_number, str):
        return False
    cc_number = cc_number.replace(" ", "")
    def digits_of(n): return [int(d) for d in n]
    digits = digits_of(cc_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(str(d*2)))
    return checksum % 10 == 0

def ai_validation(data):
    # Placeholder: AI/LLM validation logic
    # Simulate heavy validation (always pass for demo)
    return True

def risk_score(data):
    # Simple risk scoring: more alerts = higher risk
    score = 0
    if data.get("refund_amount", 0) > 10000:
        score += 30
    if data.get("ssn") in {"123-45-6789", "987-65-4321"}:
        score += 40
    if not cc_check(data.get("cc_number")):
        score += 20
    # Add more features as needed
    return min(score, 100)

def get_recent_filers():
    # Placeholder: In production, query DB or external service
    return {"user123", "user456"}

def run_ews_checks(data: Dict[str, Any]) -> Dict[str, Any]:
    results = []
    for rule_name, rule_fn in EWS_RULES:
        if rule_fn(data):
            results.append(rule_name)
    return {
        "passed": not results,
        "alerts": results,
        "risk_score": risk_score(data)
    }
