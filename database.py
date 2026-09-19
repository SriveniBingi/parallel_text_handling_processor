import sqlite3
from config import DB_NAME


# ================= CONNECTION =================
def get_connection():
    """Create and return a connection to the SQLite database."""
    return sqlite3.connect(DB_NAME, check_same_thread=False)


# ================= CREATE TABLE =================
def create_table():
    """Create table if it does not exist.
    
    Also creates an index on 'sentiment' for faster filtering/search.
    """
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
    """Wipes all records from the text_data table."""
    create_table()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM text_data")
    conn.commit()
    conn.close()


# ================= INSERT DATA =================
def insert_results(results, overwrite=False):
    """Insert processed results into database using batch processing.
    
    Uses INSERT OR REPLACE to prevent sqlite3.IntegrityError on duplicate IDs.
    """
    create_table()
    conn = get_connection()
    cursor = conn.cursor()

    if overwrite:
        cursor.execute("DELETE FROM text_data")

    batch_size = 1000
    for i in range(0, len(results), batch_size):
        batch = results[i:i + batch_size]

        # INSERT OR REPLACE handles existing IDs without crashing
        cursor.executemany("""
        INSERT OR REPLACE INTO text_data (id, text, score, sentiment)
        VALUES (?, ?, ?, ?)
        """, batch)

    conn.commit()
    conn.close()


# ================= FETCH DATA =================
def fetch_all():
    """Fetches all records, ensuring the table exists and executing the query first."""
    create_table()
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, text, score, sentiment FROM text_data")
    rows = cursor.fetchall()

    conn.close()
    return rows


# ================= SEARCH FUNCTIONS =================
def search_by_name(name):
    """Search by ID or substring in the text."""
    conn = get_connection()
    cursor = conn.cursor()

    clean_name = name.lower().replace("student_", "").replace("id_", "").strip()
    query = "SELECT * FROM text_data WHERE CAST(id AS TEXT) = ? OR text LIKE ?"
    cursor.execute(query, (clean_name, f"%{name}%"))

    results = cursor.fetchall()
    conn.close()
    return results


def search_by_sentiment(sentiment):
    """Filters records by sentiment, ignoring case sensitivity."""
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM text_data WHERE LOWER(sentiment) = LOWER(?)"
    cursor.execute(query, (sentiment.strip(),))

    results = cursor.fetchall()
    conn.close()
    return results


def search_by_keyword(keyword):
    """Finds records where the keyword exists anywhere in the text."""
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM text_data WHERE LOWER(text) LIKE LOWER(?)"
    search_term = f"%{keyword.strip()}%"

    cursor.execute(query, (search_term,))
    results = cursor.fetchall()
    conn.close()
    return results


def search_by_score(min_score):
    """Filters records with a score greater than or equal to input."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM text_data WHERE score >= ?", (min_score,))
    results = cursor.fetchall()
    conn.close()
    return results
