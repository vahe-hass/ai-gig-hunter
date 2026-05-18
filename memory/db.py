import sqlite3

conn = sqlite3.connect(
    "leads.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS leads (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    title TEXT NOT NULL,

    description TEXT,

    client_name TEXT,

    client_email TEXT,

    budget TEXT,

    url TEXT UNIQUE,

    score INTEGER DEFAULT 0
    CHECK(score >= 0 AND score <= 100),

    contacted INTEGER DEFAULT 0,

    created_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP

)
""")

conn.commit()


def save_lead(job):

    if not job.get("title"):

        print(
            "Skipping lead with missing title"
        )

        return

    try:

        cursor.execute("""
        INSERT OR IGNORE INTO leads (

            title,
            description,
            client_name,
            client_email,
            budget,
            url,
            score

        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (

            job.get("title"),

            job.get("description"),

            job.get("client_name"),

            job.get("client_email"),

            job.get("budget"),

            job.get("url"),

            int(job.get("score", 0))

        ))

        conn.commit()

        if cursor.rowcount == 0:

            print(
                f"Duplicate skipped: "
                f"{job.get('title')}"
            )

        else:

            print(
                f"Lead saved: "
                f"{job.get('title')}"
            )

    except Exception as e:

        conn.rollback()

        print(
            f"Failed to save lead: "
            f"{job.get('title')}"
        )

        print(str(e))


def get_uncontacted():

    return cursor.execute("""
    SELECT *
    FROM leads
    WHERE contacted = 0
    ORDER BY score DESC
    """).fetchall()


def mark_contacted(lead_id):

    cursor.execute("""
    UPDATE leads
    SET contacted = 1,
        updated_at = CURRENT_TIMESTAMP
    WHERE id = ?
    """, (lead_id,))

    conn.commit()


def update_score(lead_id, score):

    try:

        score = int(score)

        score = max(0, min(score, 100))

        cursor.execute("""
        UPDATE leads
        SET score = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """, (score, lead_id))

        conn.commit()

        print(
            f"Updated lead #{lead_id} "
            f"score to {score}"
        )

    except Exception as e:

        conn.rollback()

        print(
            f"Failed to update score "
            f"for lead #{lead_id}"
        )

        print(str(e))