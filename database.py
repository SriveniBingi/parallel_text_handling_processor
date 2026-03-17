import sqlite3
from config import DB_NAME

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_feedback(
        student_id INTEGER,
        student_name TEXT,
        feedback TEXT,
        score INTEGER,
        sentiment TEXT
    )
    """)

    # Index for performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_name ON student_feedback(student_name)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sentiment ON student_feedback(sentiment)")

    conn.commit()
    conn.close()


def clear_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM student_feedback")
    conn.commit()
    conn.close()


def insert_results(results):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executemany("""
    INSERT INTO student_feedback
    VALUES (?, ?, ?, ?, ?)
    """, results)

    conn.commit()
    conn.close()