import sqlite3
from config import DB_NAME


# ================= CONNECTION =================
def get_connection():
    return sqlite3.connect(DB_NAME)


# ================= CREATE TABLE =================
def create_table():

    conn = get_connection()
    cursor = conn.cursor()

    # Generic table (no student-specific fields)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS text_data(
        id INTEGER,
        text TEXT,
        score INTEGER,
        sentiment TEXT
    )
    """)

    # Index for faster search
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sentiment ON text_data(sentiment)")

    conn.commit()
    conn.close()


# ================= CLEAR TABLE =================
def clear_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM text_data")

    conn.commit()
    conn.close()


# ================= INSERT DATA =================
def insert_results(results):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executemany("""
    INSERT INTO text_data
    VALUES (?, ?, ?, ?)
    """, results)

    conn.commit()
    conn.close()