import sqlite3
from config.logger import logger

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

    client_website TEXT,

    url TEXT UNIQUE,

    score INTEGER DEFAULT 0
    CHECK(score >= 0 AND score <= 100),

    contacted INTEGER DEFAULT 0,

    audit_score INTEGER,

    audit_notes TEXT,

    created_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP

)
""")

conn.commit()


def save_lead(job):

    if not job.get("title"):

        logger.info("Skipping lead with missing title")

        return

    try:

        cursor.execute("""
        INSERT OR IGNORE INTO leads (

            title,
            description,
            client_name,
            client_email,
            client_website,
            url,
            score

        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (

            job.get("title"),

            job.get("description"),

            job.get("client_name"),

            job.get("client_email"),

            job.get("client_website"),

            job.get("url"),

            int(job.get("score", 0))

        ))

        conn.commit()

        if cursor.rowcount == 0:

            logger.info(f"Duplicate skipped: {job.get('title')}")

        else:

            logger.info(f"Lead saved: {job.get('title')}")

    except Exception as e:

        conn.rollback()

        logger.warning(f"Failed to save lead: {job.get('title')}")
        logger.exception(e)


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

        logger.info(f"Updated lead #{lead_id} score to {score}")

    except Exception as e:

        conn.rollback()

        logger.warning(f"Failed to update score for lead #{lead_id}")
        logger.exception(e)


def get_unaudited_websites():

    cursor.execute("""

    SELECT *

    FROM leads

    WHERE client_website IS NOT NULL

    AND audit_score IS NULL

    """)

    columns = [
        column[0]
        for column in cursor.description
    ]

    rows = cursor.fetchall()

    return [
        dict(zip(columns, row))
        for row in rows
    ]


def update_website_audit(

    lead_id,

    audit_score,

    audit_notes

):

    cursor.execute("""

    UPDATE leads

    SET
        audit_score = ?,
        audit_notes = ?,
        updated_at = CURRENT_TIMESTAMP

    WHERE id = ?

    """, (

        audit_score,
        audit_notes,
        lead_id

    ))

    conn.commit()


def get_leads_missing_email():

    cursor.execute("""

    SELECT *

    FROM leads

    WHERE client_website IS NOT NULL

    AND client_email IS NULL

    """)

    columns = [
        column[0]
        for column in cursor.description
    ]

    rows = cursor.fetchall()

    return [
        dict(zip(columns, row))
        for row in rows
    ]


def update_lead_email(

    lead_id,

    email

):

    cursor.execute("""

    UPDATE leads

    SET
        client_email = ?,
        updated_at = CURRENT_TIMESTAMP

    WHERE id = ?

    """, (

        email,
        lead_id

    ))

    conn.commit()


def get_sales_ready_leads():

    cursor.execute("""

    SELECT *

    FROM leads

    WHERE contacted = 0

    AND client_email IS NOT NULL

    AND (
        score >= 60
        OR audit_score <= 70
    )

    ORDER BY created_at DESC

    """)

    columns = [
        column[0]
        for column in cursor.description
    ]

    rows = cursor.fetchall()

    return [
        dict(zip(columns, row))
        for row in rows
    ]