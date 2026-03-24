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

def clear_table():
    """Wipes all records from the text_data table."""
    create_table() # Ensure it exists before trying to delete
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM text_data")
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
    """Fetches all records, ensuring the table exists first."""
    create_table()
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM text_data")
    rows = cursor.fetchall()

    conn.close()
    return rows

# ================= SEARCH FUNCTIONS (REQUIRED BY main.py) =================

def search_by_name(name):
    conn = get_connection()
    cursor = conn.cursor()
    
    # This logic strips 'student_' or 'id_' from the input to find the raw ID
    clean_name = name.lower().replace("student_", "").replace("id_", "").strip()
    
    # Search the ID column for the number OR the Text column for the string
    query = "SELECT * FROM text_data WHERE CAST(id AS TEXT) = ? OR text LIKE ?"
    cursor.execute(query, (clean_name, f"%{name}%"))
    
    results = cursor.fetchall()
    conn.close()
    return results

def search_by_sentiment(sentiment):
    """Filters records by sentiment, ignoring case sensitivity."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # LOWER() converts the database value to lowercase 
    # and we compare it to the lowercase version of the user's input
    query = "SELECT * FROM text_data WHERE LOWER(sentiment) = LOWER(?)"
    
    cursor.execute(query, (sentiment.strip(),))
    results = cursor.fetchall()
    conn.close()
    return results

def search_by_keyword(keyword):
    """Finds records where the keyword exists anywhere in the text."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # The % symbols are wildcards. 
    # %better% means: [Anything] + better + [Anything]
    query = "SELECT * FROM text_data WHERE LOWER(text) LIKE LOWER(?)"
    
    # We wrap the keyword in % symbols before sending it to SQL
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