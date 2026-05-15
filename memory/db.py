import sqlite3

conn = sqlite3.connect("leads.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS leads (
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
    contacted INTEGER DEFAULT 0
)
""")

def save_lead(job):
    cursor.execute(
        "INSERT INTO leads (title, description) VALUES (?, ?)",
        (job["title"], job["description"])
    )
    conn.commit()

def get_uncontacted():
    return cursor.execute(
        "SELECT * FROM leads WHERE contacted = 0"
    ).fetchall()

def mark_contacted(lead_id):
    cursor.execute(
        "UPDATE leads SET contacted = 1 WHERE id = ?",
        (lead_id,)
    )
    conn.commit()