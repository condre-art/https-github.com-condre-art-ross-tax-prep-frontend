PRAGMA foreign_keys = ON;

-- Tenants (white-label)
CREATE TABLE IF NOT EXISTS tenants (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  slug TEXT NOT NULL UNIQUE,
  brand_name TEXT,
  domain TEXT,
  status TEXT NOT NULL DEFAULT 'active',
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Users
CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY,
  tenant_id TEXT,
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  role TEXT NOT NULL DEFAULT 'admin', -- admin|staff|partner|client
  status TEXT NOT NULL DEFAULT 'active',
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE SET NULL
);

-- Licenses
CREATE TABLE IF NOT EXISTS licenses (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  license_type TEXT NOT NULL, -- affiliate|reseller|enterprise
  status TEXT NOT NULL,       -- pending|active|expired|revoked
  seats INTEGER NOT NULL DEFAULT 1,
  starts_at TEXT NOT NULL,
  expires_at TEXT,
  meta_json TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_licenses_tenant_status ON licenses(tenant_id, status);
CREATE INDEX IF NOT EXISTS idx_licenses_tenant_expires ON licenses(tenant_id, expires_at);

-- Certificates (PDF stored in R2; key stored here)
CREATE TABLE IF NOT EXISTS certificates (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  title TEXT NOT NULL,
  type TEXT NOT NULL,   -- irs|security|lms|operational|state
  status TEXT NOT NULL, -- active|expired|missing|revoked
  issued_at TEXT NOT NULL,
  expires_at TEXT,
  file_key TEXT,        -- R2 key
  hash_sha256 TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_cert_tenant_status ON certificates(tenant_id, status);

-- Badges (icons can be public URL or R2 key)
CREATE TABLE IF NOT EXISTS badges (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  name TEXT NOT NULL,
  icon_key TEXT,
  icon_url TEXT,
  status TEXT NOT NULL DEFAULT 'active', -- active|expired|revoked
  issued_at TEXT NOT NULL,
  expires_at TEXT,
  display_order INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_badges_tenant_status ON badges(tenant_id, status);

-- Compliance runs
CREATE TABLE IF NOT EXISTS compliance_runs (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  percentage INTEGER NOT NULL DEFAULT 0,
  overall TEXT NOT NULL, -- compliant|partial|non-compliant
  results_json TEXT NOT NULL DEFAULT '{}',
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
);

-- Audit log
CREATE TABLE IF NOT EXISTS audit_log (
  id TEXT PRIMARY KEY,
  tenant_id TEXT,
  actor_user_id TEXT,
  action TEXT NOT NULL,
  target_type TEXT,
  target_id TEXT,
  ip TEXT,
  user_agent TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_audit_tenant ON audit_log(tenant_id, created_at);
