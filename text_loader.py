import csv
def read_csv(file_path):
    rows = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            # Check the first line to see if it's a standard CSV or the Kaggle format
            first_line = file.readline()
            file.seek(0) # Go back to start of file

            # Case 1: Kaggle Sentiment Format (Sentence @sentiment)
            if "@" in first_line and "," not in first_line:
                for idx, line in enumerate(file):
                    if "@" in line:
                        # Split at the last '@' to get text and label
                        parts = line.rsplit("@", 1)
                        rows.append((f"K-{idx}", parts[0].strip()))
            
            # Case 2: Standard CSV (Your original logic)
            else:
                reader = csv.DictReader(file)
                cols = reader.fieldnames
                id_col = "student_id" if "student_id" in cols else cols[0]
                text_col = "feedback" if "feedback" in cols else (cols[1] if len(cols) > 1 else cols[0])

                for row in reader:
                    try:
                        rows.append((row[id_col], row[text_col]))
                    except KeyError:
                        continue
                        
    except Exception as e:
        print(f"Error reading dataset: {e}")
        
    return rows

def chunk_data(data, chunk_size):
    """
    Memory-efficient chunking using a generator.
    Yields slices of the data instead of creating a massive list of lists.
    """
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]