"""
seed_data.py: Seed the application with AI-generated, verified, and accurate data for users, clients, tax, and credit modules.
Includes:
- AI data generation stubs (replace with real AI calls in production)
- Example AI prompts for tax/credit data
- SQL/Python code to insert all seed data
- EWS 2.0 (Early Warning System) and CADE2 mock logic
- Database insertion and workflow triggering
"""
import random
from datetime import datetime
from blueprint import User, Role, TenantConfig
import sqlite3
from workflows import on_new_credit_report

# Example AI prompt for tax data generation
AI_PROMPT_TAX = "Generate a realistic tax profile for a US taxpayer, including income, deductions, credits, and refund estimate."
AI_PROMPT_CREDIT = "Generate a realistic credit report for a US consumer, including scores, trade-lines, and derogatory marks."

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

def cade2_pre_submission_check(tax_profile):
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

# Database insertion and workflow triggering
DB_PATH = "demo.db"  # Use the same DB as schema_seed.sql

def insert_user(conn, user: User):
    conn.execute("INSERT OR IGNORE INTO users (id, email, password_hash, role, tenant_id, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (user.id, user.email, "hashed", user.role, user.tenant_id, user.status, datetime.now(), datetime.now()))

def insert_tenant(conn, tenant: TenantConfig):
    conn.execute("INSERT OR IGNORE INTO tenants (id, name, slug, brand_name, domain, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (tenant.tenant_id, tenant.brand_name, tenant.brand_name.lower(), tenant.brand_name, None, "active", datetime.now(), datetime.now()))

def insert_tax_profile(conn, user_id, tax_profile):
    conn.execute("INSERT INTO tax_profiles (user_id, income, deductions, credits, refund_estimate, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, tax_profile["income"], str(tax_profile["deductions"]), str(tax_profile["credits"]), tax_profile["refund_estimate"], datetime.now()))

def insert_credit_report(conn, user_id, credit_report):
    conn.execute("INSERT INTO credit_reports (user_id, score, tradelines, derogatory, created_at) VALUES (?, ?, ?, ?, ?)",
        (user_id, credit_report["score"], str(credit_report["tradelines"]), str(credit_report["derogatory"]), datetime.now()))

def trigger_workflows(user_id, tax_profile, credit_report):
    # Example: trigger credit report workflow
    print(on_new_credit_report(user_id, credit_report))
    # Add more workflow triggers as needed

# Seed process
if __name__ == "__main__":
    # 1. Run schema migration (apply schema_seed.sql)
    import os
    SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema_seed.sql")
    conn = sqlite3.connect(DB_PATH)
    with open(SCHEMA_PATH, "r") as f:
        schema_sql = f.read()
    conn.execute script(schema_sql)
    print("Database schema migrated.")

    # 2. Print sample AI-generated data (reference/demo)
    for i in range(5):
        tax_profile = ai_generate_tax_profile()
        credit_report = ai_generate_credit_report()
        print(f"Tax Profile {i+1}: {tax_profile}")
        print(f"Credit Report {i+1}: {credit_report}")
        print("EWS Flags:", ews_check(tax_profile))
        print("CADE2 Issues:", cade2_presubmission_check(tax_profile))
        print("Refund Maximization Suggestions:", maximize_refund(tax_profile))
        print("---")

    # 3. Seed base reference data (tenants, users, roles)
    tenant = TenantConfig(tenant_id="t1", brand_name="Acme Tax", theme="ios", features=["payroll", "credit"])
    insert_tenant(conn, tenant)
    users = [User(id=i+2, email=f"user{i+2}@example.com", name=f"User{i+2}", role="client", tenant_id="t1") for i in range(5)]
    for user in users:
        insert_user(conn, user)

    # 4. Seed live operational data (tax profiles, credit reports, workflows)
    for user in users:
        tax_profile = ai_generate_tax_profile()
        credit_report = ai_generate_credit_report()
        insert_tax_profile(conn, user.id, tax_profile)
        insert_credit_report(conn, user.id, credit_report)
        trigger_workflows(user.id, tax_profile, credit_report)
    conn.commit()
    conn.close()
    print("Seed data inserted and workflows triggered.")
