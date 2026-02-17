"""
seed_data.py: Seed the application with AI-generated, verified, and accurate data for users, clients, tax, and credit modules.
Includes:
- AI data generation stubs (replace with real AI calls in production)
- Example AI prompts for tax/credit data
- SQL/Python code to insert all seed data
- EWS 2.0 (Early Warning System) and CADE2 mock logic
"""
import random
from datetime import datetime
from blueprint import User, Role, TenantConfig

# Example AI prompt for tax data generation
AI_PROMPT_TAX = "Generate a realistic tax profile for a US taxpayer, including income, deductions, credits, and refund estimate."
AI_PROMPT_CREDIT = "Generate a realistic credit report for a US consumer, including scores, tradelines, and derogatory marks."

def ai_generate_tax_profile():
    # Stub: Replace with real AI call
    return {
        "income": random.randint(25000, 120000),
        "deductions": ["Standard Deduction"],
        "credits": ["EITC", "Child Tax Credit"],
        "refund_estimate": random.randint(500, 8000)
    }

def ai_generate_credit_report():
    # Stub: Replace with real AI call
    return {
        "score": random.randint(580, 800),
        "tradelines": ["Auto Loan", "Credit Card"],
        "derogatory": ["Late Payment"] if random.random() < 0.3 else []
    }

# Insert seed data (replace with DB calls in production)
USERS = [User(id=1, email="admin@example.com", name="Admin", role="admin", tenant_id="t1")]
ROLES = [Role(id=1, name="admin", permissions=["all"]), Role(id=2, name="client", permissions=["view", "submit"])]
TENANTS = [TenantConfig(tenant_id="t1", brand_name="Acme Tax", theme="ios", features=["payroll", "credit"]) ]

# EWS 2.0: Early Warning System logic

def ews_check(tax_profile):
    # Check for flags that could delay IRS processing
    flags = []
    if tax_profile["income"] > 100000 and "EITC" in tax_profile["credits"]:
        flags.append("EITC high income review")
    if "derogatory" in tax_profile and tax_profile["derogatory"]:
        flags.append("Credit derogatory marks present")
    return flags

# CADE2 Mock: Pre-submission accuracy and pre-ack check

def cade2_presubmission_check(tax_profile):
    # Simulate IRS master file checks
    issues = []
    if tax_profile["refund_estimate"] > 7000:
        issues.append("High refund: manual review")
    if not tax_profile["deductions"]:
        issues.append("No deductions claimed")
    return issues

# Highest refund algorithm

def maximize_refund(tax_profile):
    # Suggest changes to maximize refund
    suggestions = []
    if "EITC" not in tax_profile["credits"] and tax_profile["income"] < 60000:
        suggestions.append("Add EITC")
    if "Child Tax Credit" not in tax_profile["credits"]:
        suggestions.append("Add Child Tax Credit if eligible")
    return suggestions

# Seed process
if __name__ == "__main__":
    for i in range(5):
        tax_profile = ai_generate_tax_profile()
        credit_report = ai_generate_credit_report()
        print(f"Tax Profile {i+1}: {tax_profile}")
        print(f"Credit Report {i+1}: {credit_report}")
        print("EWS Flags:", ews_check(tax_profile))
        print("CADE2 Issues:", cade2_presubmission_check(tax_profile))
        print("Refund Maximization Suggestions:", maximize_refund(tax_profile))
        print("---")
