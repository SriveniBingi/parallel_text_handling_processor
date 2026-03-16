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


def fetch_all():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM student_feedback")
    data = cursor.fetchall()

    conn.close()

    return data


def search_by_name(name):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM student_feedback WHERE LOWER(student_name) =LOWER(?)",
        ( name,)
    )

    data = cursor.fetchall()
    conn.close()

    return data


def search_by_sentiment(sentiment):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM student_feedback WHERE sentiment = ?",
        (sentiment,)
    )

    data = cursor.fetchall()
    conn.close()
    
    return data

# Search by Keyword in Feedback
def search_by_keyword(keyword):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM student_feedback WHERE feedback LIKE ?",
        ('%' + keyword + '%',)
    )

    data = cursor.fetchall()
    conn.close()

def search_by_score(score):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM student_feedback WHERE score <= ?",
        (score,)
    )

    results = cursor.fetchall()
    conn.close()

    return results