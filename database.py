import sqlite3
from config import DB_NAME


def create_connection():
    return sqlite3.connect(DB_NAME)


def create_table():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_feedback (
        student_id INTEGER,
        student_name TEXT,
        feedback TEXT,
        score INTEGER,
        sentiment TEXT
    )
    """)

    conn.commit()
    conn.close()


def clear_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM student_feedback")
    conn.commit()
    conn.close()


def insert_results(results):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.executemany(
    "INSERT INTO student_feedback VALUES (?, ?, ?, ?, ?)",
    results
)

    conn.commit()
    conn.close()


def fetch_all():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student_feedback")
    rows = cursor.fetchall()
    conn.close()
    return rows


def search_by_name(name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM student_feedback WHERE LOWER(student_name)=LOWER(?)",
        (name,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows
