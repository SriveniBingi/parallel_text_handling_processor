import csv

def export_to_csv(data, filename="results.csv"):

    with open(filename, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Student ID",
            "Student Name",
            "Feedback",
            "Score",
            "Sentiment"
        ])

        for row in data:
            writer.writerow(row)

    print(f"\nResults exported to {filename}")
