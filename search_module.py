import csv


def export_to_csv(data, filename="processed_students.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Student ID", "Name", "Feedback", "Score", "Sentiment"])
        writer.writerows(data)

    print(f"\nResults exported to {filename}")
