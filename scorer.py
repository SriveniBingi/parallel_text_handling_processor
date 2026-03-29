import re
from config import POSITIVE_WORDS, NEGATIVE_WORDS,NEGATIONS, INTENSIFIERS

def calculate_score(text):
    """
    Analyze text and return:
    - positive word count
    - negative word count
    - total score
    - sentiment label
    """

    # 🔹 Better tokenization (handles punctuation properly)
    words = re.findall(r'\b[\w-]+\b', text.lower())

    total_score = 0
    pos_count = 0
    neg_count = 0

    i = 0
    while i < len(words):
        word = words[i]

        multiplier = 1
        invert = False

        # ✅ HANDLE NEGATION + INTENSIFIER TOGETHER
        if word in NEGATIONS and i + 1 < len(words):
            next_word = words[i + 1]

            # Case 1: not good
            if next_word in POSITIVE_WORDS or next_word in NEGATIVE_WORDS:
                invert = True
                i += 1
                word = next_word

            # Case 2: not very good
            elif next_word in INTENSIFIERS and i + 2 < len(words):
                multiplier = 2
                invert = True
                i += 2
                word = words[i]

        # ✅ HANDLE NORMAL INTENSIFIER
        elif word in INTENSIFIERS and i + 1 < len(words):
            multiplier = 2
            i += 1
            word = words[i]

        # ✅ SCORING
        if word in POSITIVE_WORDS:
            score = 1 * multiplier
            if invert:
                score *= -1
            total_score += score
            pos_count += 1

        elif word in NEGATIVE_WORDS:
            score = -1 * multiplier
            if invert:
                score *= -1
            total_score += score
            neg_count += 1

        i += 1
    # 🔹 Final sentiment
    if total_score >= 2:
        sentiment = "Strong Positive"
    elif total_score == 1:
        sentiment = "Positive"
    elif total_score == 0:
        sentiment = "Neutral"
    elif total_score == -1:
        sentiment = "Negative"
    else:  # total_score <= -2
        sentiment = "Strong Negative"
        
    return pos_count, neg_count, total_score, sentiment



# ================= PROCESS CHUNK =================
def process_chunk(chunk):
    """
    Process a chunk of data.
    This runs in parallel across multiple processes.
    """

    results = []

    for row in chunk:
        text = row[1]   # extract text

        # ✅ correct function + correct order
        pos_count, neg_count, total_score, sentiment = calculate_score(text)

        results.append((
            row[0],          # id
            text,
            total_score,
            sentiment
        ))

    return results