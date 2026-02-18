import sqlite3
import json

DB_PATH = "demo.db"  # Path to the demo database
EXPORT_PATH = "client_export.json"

def export_clients():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    clients = []
    # Export all users with role 'client'
    for user in conn.execute("SELECT * FROM users WHERE role = 'client'"):
        user_dict = dict(user)
        # Get tax profiles
        tax_profiles = [dict(row) for row in conn.execute("SELECT * FROM tax_profiles WHERE user_id = ?", (user["id"],))]
        # Get credit reports
        credit_reports = [dict(row) for row in conn.execute("SELECT * FROM credit_reports WHERE user_id = ?", (user["id"],))]
        user_dict["tax_profiles"] = tax_profiles
        user_dict["credit_reports"] = credit_reports
        clients.append(user_dict)
    with open(EXPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(clients, f, indent=2, default=str)
    print(f"Exported {len(clients)} clients to {EXPORT_PATH}")

if __name__ == "__main__":
    export_clients()
