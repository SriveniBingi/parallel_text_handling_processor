import csv
import random
import os

os.makedirs("data", exist_ok=True)

subjects = ["assignments", "teaching", "course", "faculty", "labs", "exams"]
positive_words = ["excellent", "amazing", "good", "great", "helpful"]
negative_words = ["poor", "bad", "terrible", "awful", "difficult"]
neutral_words = ["okay", "average", "normal", "fine"]

NUMBER_OF_RECORDS = 50000

with open("data/students.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["student_id", "student_name", "feedback"])

    for i in range(1, NUMBER_OF_RECORDS + 1):
        name = f"Student_{i}"

        sentiment_type = random.choice(["positive", "negative", "neutral"])
        subject = random.choice(subjects)

        if sentiment_type == "positive":
            word = random.choice(positive_words)
            feedback = f"The {subject} was {word}"

        elif sentiment_type == "negative":
            word = random.choice(negative_words)
            feedback = f"The {subject} was {word}"

        else:
            word = random.choice(neutral_words)
            feedback = f"The {subject} was {word}"

        writer.writerow([i, name, feedback])

print(f"{NUMBER_OF_RECORDS} records generated successfully!")