import csv

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


def chunk_data(data, chunk_size):
    chunks = []
    for i in range(0, len(data), chunk_size):
        chunks.append(data[i:i + chunk_size])
    return chunks
