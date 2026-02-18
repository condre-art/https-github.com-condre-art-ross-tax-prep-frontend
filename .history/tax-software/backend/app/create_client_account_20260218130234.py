"""
Script to create a secure client login account with a temporary passcode DN12345! and upload a sample client to the users table.
"""
import sqlite3
import hashlib
import uuid
from datetime import datetime

DB_PATH = "demo.db"  # Use the same DB as the app
TEMP_PASS = "DN12345!"
TENANT_ID = "t1"
CLIENT_EMAIL = "client1@example.com"
CLIENT_NAME = "Client One"

def hash_password(password: str) -> str:
    # Simple SHA256 hash for demo (replace with bcrypt/argon2 in production)
    return hashlib.sha256(password.encode()).hexdigest()

def create_client():
    user_id = str(uuid.uuid4())
    password_hash = hash_password(TEMP_PASS)
    now = datetime.now().isoformat()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO users (id, tenant_id, email, password_hash, role, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(email) DO UPDATE SET password_hash=excluded.password_hash, updated_at=excluded.updated_at
        """,
        (user_id, TENANT_ID, CLIENT_EMAIL, password_hash, "client", "active", now, now)
    )
    conn.commit()
    conn.close()
    print(f"Client account created: {CLIENT_EMAIL} (temp pass: {TEMP_PASS})")

if __name__ == "__main__":
    create_client()