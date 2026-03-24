import csv
import random
import os

os.makedirs("data", exist_ok=True)

positive_feedback = [
    "The course was excellent and amazing",
    "I love the teaching style it is great",
    "The sessions were very good and helpful",
    "Amazing practical exposure and great learning",
    "Excellent support from faculty"
]

negative_feedback = [
    "The teaching was poor and bad",
    "I had a terrible experience",
    "The course content was awful",
    "Bad explanation and poor support",
    "I hate the scheduling system"
]

neutral_feedback = [
    "The course was okay",
    "It was an average experience",
    "Nothing special about the sessions",
    "The class was normal",
    "It was fine overall"
]

all_feedback = positive_feedback + negative_feedback + neutral_feedback
feedback = random.choice(positive_feedback*3 + negative_feedback*2 + neutral_feedback*2)
NUMBER_OF_RECORDS = 50000

with open("data/students.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["student_id", "student_name", "feedback"])

    for i in range(1, NUMBER_OF_RECORDS + 1):
        name = f"Student_{i}"
        feedback = random.choice(all_feedback)
        writer.writerow([i, name, feedback])

print(f"{NUMBER_OF_RECORDS} student records generated successfully!")
