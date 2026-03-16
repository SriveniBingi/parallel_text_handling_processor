import re
from config import POSITIVE_WORDS, NEGATIVE_WORDS


def score_feedback(row):
    """
    Calculate sentiment score for a single feedback row.
    Input: (student_id, student_name, feedback)
    Output: (student_id, student_name, feedback, score, sentiment)
    """

    student_id, name, feedback = row
    score = 0

    # Count positive words
    for word in POSITIVE_WORDS:
        score += len(re.findall(rf"\b{word}\b", feedback, re.IGNORECASE))

    # Count negative words
    for word in NEGATIVE_WORDS:
        score -= len(re.findall(rf"\b{word}\b", feedback, re.IGNORECASE))

    # Assign sentiment label
    if score > 0:
        sentiment = "Positive"
    elif score < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return (student_id, name, feedback, score, sentiment)


def process_chunk(chunk):
    """
    Process a chunk of feedback rows in parallel.
    """
    results = []

    for row in chunk:
        scored_row = score_feedback(row)
        results.append(scored_row)

    return results


def detect_alerts(results):
    """
    Detect negative feedback alerts.
    """
    alerts = []

    for row in results:
        student_id, name, feedback, score, sentiment = row

        if sentiment == "Negative":
            alerts.append((student_id, name, feedback))

    return alerts