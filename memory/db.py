import sqlite3

conn = sqlite3.connect("leads.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    client_name TEXT,
    client_email TEXT,
    budget TEXT,
    score INTEGER DEFAULT 0 CHECK(score >= 0 AND score <= 100),
    contacted INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

def save_lead(job):
    
    if not job.get("title"):
        print("Skipping lead with missing title")
        return
    try:
        cursor.execute("""
        INSERT INTO leads (
            title,
            description,
            client_name,
            client_email,
            budget,
            score
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """, (

            job.get("title"),
            job.get("description"),
            job.get("client_name"),
            job.get("client_email"),
            job.get("budget"),
            int(job.get("score", 0))

        ))

        conn.commit()
        print(f"Lead saved: {job.get('title')}")

    except Exception as e:

        conn.rollback()
        print(f"Failed to save lead: {job.get('title')}")
        print(str(e))

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