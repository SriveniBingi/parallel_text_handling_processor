import re
from config import POSITIVE_WORDS, NEGATIVE_WORDS


# ================= SCORE FUNCTION =================
def score_feedback(row):
    # Now we accept only (id, text)
    id, text = row

    score = 0

    # Count positive words
    for word in POSITIVE_WORDS:
        score += len(re.findall(rf"\b{word}\b", text, re.IGNORECASE))

    # Count negative words
    for word in NEGATIVE_WORDS:
        score -= len(re.findall(rf"\b{word}\b", text, re.IGNORECASE))

    # Decide sentiment
    if score > 0:
        sentiment = "Positive"
    elif score < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    # Return updated structure
    return (id, text, score, sentiment)


# ================= PROCESS CHUNK =================
def process_chunk(chunk):
    results = []

    for row in chunk:
        results.append(score_feedback(row))

    return results