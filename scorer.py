import re
from config import POSITIVE_WORDS, NEGATIVE_WORDS

# ================= PRECOMPILE WORD SETS =================
# Convert lists to sets for faster lookup (O(1) time)
POS_SET = set(word.lower() for word in POSITIVE_WORDS)
NEG_SET = set(word.lower() for word in NEGATIVE_WORDS)


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
    words = re.findall(r'\b\w+\b', text.lower())

    score = 0

    # ================= FAST COUNT =================
    # Loop once instead of multiple regex calls
    for word in words:
        if word in POS_SET:
            score += 1
        elif word in NEG_SET:
            score -= 1

    # ================= SENTIMENT DECISION =================
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