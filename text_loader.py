import csv
from config import CHUNK_SIZE


def read_csv(file_path):
    rows = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
         reader = csv.DictReader(file)
         for row in reader:
            rows.append((
                int(row["student_id"]),
                row["student_name"],
                row["feedback"]
            ))
    except Exception as e:
        print("Error reading CSV:",e)
        
    return rows


def chunk_data(data):
    chunks = []
    for i in range(0, len(data), CHUNK_SIZE):
        chunks.append(data[i:i + CHUNK_SIZE])
    return chunks
