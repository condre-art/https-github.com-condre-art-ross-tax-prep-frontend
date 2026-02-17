import sqlite3

# Example migration script for SQLite
conn = sqlite3.connect('yourdb.sqlite')
cursor = conn.cursor()

with open('schema.sql', 'r') as f:
    sql = f.read()
    cursor.executescript(sql)

conn.commit()
conn.close()
print("Migration complete.")
