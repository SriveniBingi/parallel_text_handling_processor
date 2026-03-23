import re
from config import POSITIVE_WORDS, NEGATIVE_WORDS

# ================= PRECOMPILE WORD SETS =================
# Convert lists to sets for faster lookup (O(1) time)
POS_SET = set(word.lower() for word in POSITIVE_WORDS)
NEG_SET = set(word.lower() for word in NEGATIVE_WORDS)

NEGATIONS = {"not", "no", "never"}
INTENSIFIERS = {"very", "extremely", "super"}

# ================= SCORE FUNCTION =================
def score_feedback(row):
    """
    Calculate sentiment score for a single row.
    Input: (id, text)
    Output: (id, text, score, sentiment)
    """

    id, text = row

    # ================= CLEAN & TOKENIZE =================
    # Convert to lowercase and extract words
    words = text.lower().split()

    score = 0
    i = 0

    while i < len(words):
        word = words[i]

        multiplier = 1
        invert = False

        # 🔹 Handle negation (not good → negative)
        if word in NEGATIONS and i + 1 < len(words):
            invert = True
            i += 1
            word = words[i]

        # 🔹 Handle intensifier (very good → strong positive)
        if word in INTENSIFIERS and i + 1 < len(words):
            multiplier = 2
            i += 1
            word = words[i]

        # 🔹 Apply scoring
        if word in POS_SET:
            val = 1 * multiplier
            if invert:
                val *= -1
            score += val

        elif word in NEG_SET:
            val = -1 * multiplier
            if invert:
                val *= -1
            score += val

        i += 1

    # ================= FINAL SENTIMENT =================
    if score > 0:
        sentiment = "Positive"
    elif score < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return (id, text, score, sentiment)


# ================= PROCESS CHUNK =================
def process_chunk(chunk):
    """
    Process a chunk of data.
    This runs in parallel across multiple processes.
    """

    results = []

    for row in chunk:
        results.append(score_feedback(row))

    return results