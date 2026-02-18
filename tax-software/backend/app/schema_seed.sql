-- Schema for seed_data.py demo DB
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    email TEXT NOT NULL,
    password_hash TEXT,
    role TEXT,
    tenant_id TEXT,
    status TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE IF NOT EXISTS tenants (
    id TEXT PRIMARY KEY,
    name TEXT,
    slug TEXT,
    brand_name TEXT,
    domain TEXT,
    status TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE IF NOT EXISTS tax_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    income INTEGER,
    deductions TEXT,
    credits TEXT,
    refund_estimate INTEGER,
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS credit_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    score INTEGER,
    tradelines TEXT,
    derogatory TEXT,
    created_at TEXT
);
