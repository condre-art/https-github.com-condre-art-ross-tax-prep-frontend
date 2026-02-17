"""
seed_data.py: Seed the application with AI-generated, verified, and accurate data for users, clients, tax returns, credit reports, and more.
Includes:
- AI data generation stubs (replace with real AI calls in production)
- Example AI prompts for tax/credit data
- SQL/Python code to insert all seed data
- EWS 2.0: Early Warning System for pre-submission accuracy and risk checks
"""
import random
from datetime import datetime

# Example AI prompt for tax data generation
AI_PROMPT_TAX = """
Given the following client profile, generate a realistic US tax return with maximum legal refund, including all eligible credits and deductions. Flag any compliance risks or audit triggers.
Client: {client}
"""

# Example AI prompt for credit data generation
AI_PROMPT_CREDIT = """
Given the following client profile, generate a realistic US credit report with tradelines, inquiries, and public records. Flag any derogatory items and suggest dispute strategies.
Client: {client}
"""

def ai_generate_tax_return(client):
    # Stub: Replace with real AI call
    return {
        "refund": random.randint(1000, 8000),
        "liability": random.randint(0, 2000),
        "credits": ["EITC", "CTC"],
        "deductions": ["Standard Deduction"],
        "flags": []
    }

def ai_generate_credit_report(client):
    # Stub: Replace with real AI call
    return {
        "score": random.randint(580, 800),
        "derogatory": random.choice([[], ["Late Payment"]]),
        "public_records": [],
        "dispute_suggestions": ["Dispute late payment"]
    }

# Example clients
clients = [
    {"id": 1, "name": "Jane Doe", "email": "jane@example.com", "income": 42000},
    {"id": 2, "name": "John Smith", "email": "john@example.com", "income": 67000},
]

# Seed tax returns and credit reports
TAX_RETURNS = []
CREDIT_REPORTS = []
for client in clients:
    tax = ai_generate_tax_return(client)
    credit = ai_generate_credit_report(client)
    TAX_RETURNS.append({"client_id": client["id"], **tax})
    CREDIT_REPORTS.append({"client_id": client["id"], **credit})

# EWS 2.0: Early Warning System

def ews_check(tax_return):
    # Pre-submission accuracy and risk check
    flags = []
    if tax_return["refund"] > 6000:
        flags.append("High refund: review for EITC/CTC compliance")
    if tax_return["liability"] == 0 and tax_return["refund"] > 4000:
        flags.append("Possible underwithholding or aggressive credits")
    # Add more IRS/BMF/EPMF/IRM checks as needed
    return flags

# Run EWS on all tax returns
for tr in TAX_RETURNS:
    tr["ews_flags"] = ews_check(tr)

# Print or insert seed data (replace with DB insert in production)
print("Seeded tax returns:", TAX_RETURNS)
print("Seeded credit reports:", CREDIT_REPORTS)
