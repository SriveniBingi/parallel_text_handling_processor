import sqlite3
from config import DB_NAME


# ================= CONNECTION =================
def get_connection():
    """
    Create and return a connection to the SQLite database.
    """
    return sqlite3.connect(DB_NAME)


# ================= CREATE TABLE =================
def create_table():
    """
    Create table if it does not exist.
    Also creates an index on 'sentiment' for faster filtering/search.
    """

    conn = get_connection()
    cursor = conn.cursor()

    # Create table structure
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS text_data(
        id INTEGER,
        text TEXT,
        score INTEGER,
        sentiment TEXT
    )
    """)

    # Create index to speed up search/filter operations
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_sentiment ON text_data(sentiment)"
    )

    conn.commit()
    conn.close()


# ================= INSERT DATA =================
def insert_results(results):
    """
    Insert processed results into database using batch processing.
    Improves performance for large datasets.
    """
    #ensures table exists
    create_table()
    conn = get_connection()
    cursor = conn.cursor()
    
    # ✅ Clear old data before inserting new
    cursor.execute("DELETE FROM text_data")
    
    # Batch insertion
    batch_size = 1000

    for i in range(0, len(results), batch_size):
        batch = results[i:i+batch_size]

        cursor.executemany("""
        INSERT INTO text_data
        VALUES (?, ?, ?, ?)
        """, batch)

    conn.commit()
    conn.close()
    
def fetch_all():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM text_data")
    rows = cursor.fetchall()

    conn.close()
    return rows