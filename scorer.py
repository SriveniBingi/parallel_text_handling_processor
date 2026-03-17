import re
from config import POSITIVE_WORDS, NEGATIVE_WORDS


def score_feedback(row):
    student_id, name, feedback = row
    score = 0

    for word in POSITIVE_WORDS:
        score += len(re.findall(rf"\b{word}\b", feedback, re.IGNORECASE))

    for word in NEGATIVE_WORDS:
        score -= len(re.findall(rf"\b{word}\b", feedback, re.IGNORECASE))

    if score > 0:
        sentiment = "Positive"
    elif score < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return (student_id, name, feedback, score, sentiment)


def process_chunk(chunk):
    results = []

    for row in chunk:
        results.append(score_feedback(row))

    return results