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
]

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
        "alerts": results
    }
