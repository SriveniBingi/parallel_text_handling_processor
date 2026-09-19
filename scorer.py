import re
from config import POSITIVE_WORDS, NEGATIVE_WORDS, NEGATIONS, INTENSIFIERS


def calculate_score(text):
    """
    Analyze text and return:
    - positive word count
    - negative word count
    - total score
    - sentiment label ('Positive', 'Negative', 'Neutral')
    """
    if not text or not isinstance(text, str):
        return 0, 0, 0, "Neutral"

    words = re.findall(r'\b[\w-]+\b', text.lower())

    total_score = 0
    pos_count = 0
    neg_count = 0

    i = 0
    while i < len(words):
        word = words[i]
        multiplier = 1
        invert = False

        # ✅ HANDLE NEGATION + INTENSIFIER TOGETHER (e.g., 'not good', 'not very good')
        if word in NEGATIONS and i + 1 < len(words):
            next_word = words[i + 1]

            # Case 1: 'not good'
            if next_word in POSITIVE_WORDS or next_word in NEGATIVE_WORDS:
                invert = True
                i += 1
                word = next_word

            # Case 2: 'not very good'
            elif next_word in INTENSIFIERS and i + 2 < len(words):
                multiplier = 2
                invert = True
                i += 2
                word = words[i]

        # ✅ HANDLE NORMAL INTENSIFIER (e.g., 'very good')
        elif word in INTENSIFIERS and i + 1 < len(words):
            multiplier = 2
            i += 1
            word = words[i]

        # ✅ SCORING & PROPER COUNT ASSIGNMENT
        if word in POSITIVE_WORDS:
            score = 1 * multiplier
            if invert:
                # 'not good' -> counts toward negative
                total_score -= score
                neg_count += 1
            else:
                total_score += score
                pos_count += 1

        elif word in NEGATIVE_WORDS:
            score = 1 * multiplier
            if invert:
                # 'not bad' -> counts toward positive
                total_score += score
                pos_count += 1
            else:
                total_score -= score
                neg_count += 1

        i += 1

    # 🔹 Standard Sentiment Categories (Matching app.py filters)
    if total_score > 0:
        sentiment = "Positive"
    elif total_score < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return pos_count, neg_count, total_score, sentiment


# ================= PROCESS CHUNK =================
def process_chunk(chunk):
    """
    Process a chunk of data.
    This runs in parallel across multiple processes.
    """
    results = []

    for row in chunk:
        text = row[1]
        pos_count, neg_count, total_score, sentiment = calculate_score(text)

        results.append((
            row[0],         # id
            text,
            total_score,
            sentiment
        ))

    return results
