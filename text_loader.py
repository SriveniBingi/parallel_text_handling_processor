import csv

def read_csv(file_path):
    """
    Reads a CSV and returns a list of (id, text) tuples.
    Attempts to find ID and Text columns dynamically.
    """
    rows = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            
            # Get fieldnames to check for column existence
            cols = reader.fieldnames
            
            # Simple logic to find the 'text' column if the hardcoded one is missing
            id_col = "student_id" if "student_id" in cols else cols[0]
            text_col = "feedback" if "feedback" in cols else (cols[1] if len(cols) > 1 else cols[0])

            for row in reader:
                try:
                    # We only need the ID and the Text for the scorer
                    rows.append((
                        row[id_col], 
                        row[text_col]
                    ))
                except KeyError:
                    continue # Skip malformed rows
                    
    except Exception as e:
        print(f"Error reading CSV: {e}")
        
    return rows


def chunk_data(data, chunk_size):
    """
    Memory-efficient chunking using a generator.
    Yields slices of the data instead of creating a massive list of lists.
    """
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]