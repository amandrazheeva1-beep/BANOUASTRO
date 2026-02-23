import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    tg_id INTEGER,
    name TEXT,
    birthdate TEXT,
    request TEXT,
    status TEXT
)
""")

conn.commit()
