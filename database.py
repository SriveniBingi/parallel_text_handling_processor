import sqlite3
from config import DB_NAME


# ================= CONNECTION =================
def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


# ================= CREATE TABLE =================
def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS text_data(
        id INTEGER PRIMARY KEY,
        text TEXT,
        score INTEGER,
        sentiment TEXT
    )
    """)

    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_sentiment ON text_data(sentiment)"
    )

    conn.commit()
    conn.close()


def clear_table():
    create_table()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM text_data")
    conn.commit()
    conn.close()


# ================= INSERT DATA =================
def insert_results(results, overwrite=False):
    create_table()
    conn = get_connection()
    cursor = conn.cursor()
    
    # Only clear if overwrite is explicitly requested
    if overwrite:
        cursor.execute("DELETE FROM text_data")
    
    batch_size = 1000
    for i in range(0, len(results), batch_size):
        batch = results[i:i+batch_size]
        cursor.executemany("""
        INSERT INTO text_data (id, text, score, sentiment)
        VALUES (?, ?, ?, ?)
        """, batch)

    conn.commit()
    conn.close()


def fetch_all():
    create_table()
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM text_data")  # <-- Fixed: execute query first
    rows = cursor.fetchall()

    conn.close()
    return rows


# ================= SEARCH FUNCTIONS =================
def search_by_name(name):
    conn = get_connection()
    cursor = conn.cursor()
    
    clean_name = name.lower().replace("student_", "").replace("id_", "").strip()
    query = "SELECT * FROM text_data WHERE CAST(id AS TEXT) = ? OR text LIKE ?"
    cursor.execute(query, (clean_name, f"%{name}%"))
    
    results = cursor.fetchall()
    conn.close()
    return results


def search_by_sentiment(sentiment):
    conn = get_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM text_data WHERE LOWER(sentiment) = LOWER(?)"
    cursor.execute(query, (sentiment.strip(),))
    results = cursor.fetchall()
    conn.close()
    return results


def search_by_keyword(keyword):
    conn = get_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM text_data WHERE LOWER(text) LIKE LOWER(?)"
    search_term = f"%{keyword.strip()}%"
    
    cursor.execute(query, (search_term,))
    results = cursor.fetchall()
    conn.close()
    return results


def search_by_score(min_score):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM text_data WHERE score >= ?", (min_score,))
    results = cursor.fetchall()
    conn.close()
    return results
