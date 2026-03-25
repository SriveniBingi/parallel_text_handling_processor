# config.py

POSITIVE_WORDS = [
    # General & Emotions
    "good", "great", "excellent", "awesome", "amazing", "fantastic", "happy", "joy", 
    "love", "wonderful", "best", "beautiful", "positive", "smile", "nice", "enjoy", 
    "like", "fortunate", "fabulous", "cool", "brilliant", "perfect", "pleasure",
    "delight", "kind", "friendly", "helpful", "clear","outstanding", "high-quality", "durable", "fast", "seamless", "innovative", 
    "recommend", "value", "authentic", "premium", "smooth", "satisfied", "responsive", "intuitive", "user-friendly", "secure", "encrypted",
    "reliable", "polished", "cutting-edge", "optimized", "compatible", "versatile", "powerful",
    
    # Business, News & Finance (Economic Sector)
    "success", "growth", "recovery", "agreement", "victory", "stable", "progress", 
    "safe", "solution", "support", "benefit", "profitable", "gain", "increase", 
    "surplus", "advance", "thriving", "sturdy", "reliable", "efficient", "wealthy",
    "prosperous", "booming", "upgraded", "effective", "productive", "leading",
    "sustainable", "breakthrough", "acquisition", "expansion", "strategy", "innovation",

    # Student, Academic & Healthcare Sector
    "helpful", "clear", "supportive", "organized", "knowledgeable", "learned", 
    "insightful", "thorough", "encouraging", "engaging", "accessible", "top",
    "healthy", "cured", "improved", "stable", "robust", "accurate", "precise",
    "mentor", "achieve", "mastery", "potential", "fluent",

    # Product, Tech & Quality Sector
    "outstanding", "high-quality", "durable", "fast", "seamless", "innovative", 
    "recommend", "value", "authentic", "premium", "smooth", "satisfied", "responsive",
    "intuitive", "user-friendly", "secure", "encrypted", "reliable", "polished",
    "cutting-edge", "optimized", "compatible", "versatile", "powerful"
]

NEGATIVE_WORDS = [
    # General & Emotions
    "bad", "poor", "worst", "terrible", "awful", "horrible", "sad", "hate", "ugly", 
    "negative", "failure", "pain", "disappointing", "angry", "unhappy", "annoying", 
    "nasty", "boring", "unfortunate", "mad", "dislike", "worried", "awful", "dreadful",
    "disgusting", "shame", "fear", "regret", "bitter", "difficult", "confusing", "frustrating", 
    "unpleasant", "uncomfortable", "disorganized","inefficient", "unreliable", "glitchy", "buggy", 
    "laggy", "vulnerable", "exposed", "outdated", "complex", "useless","waste", "slow", "defective",
    "broken", "expensive", "overpriced","scam", "fragile", "terrible", "noisy","malware", "slowdown", 
    "clunky", "unstable", "inefficient","disappointing", "angry", "unhappy", "annoying", "problem","nasty",
    "boring", "unfortunate", "mad", "dislike", "worried","difficult", "confusing", "unorganized", "slow", "vague", "hard", "useless", "rude", "harsh",
    "noisy", "distracted", "ignored", "irrelevant","sick", "ill", "infected", "deteriorated", "unresponsive", "inaccurate",
    "plagiarism", "dropout", "fail", "incomplete", "demotivated","defective", "broken", "expensive", "cheap", "waste", "slow", "buggy",
    "crash", "flawed", "overpriced", "scam", "fragile", "terrible", "noisy",
    "laggy", "vulnerable", "exposed", "outdated", "glitchy", "complex", "useless","malware", "slowdown", "clunky", "unstable", "inefficient",
    
    # Business, News & Finance (Economic Sector)
    "crisis", "conflict", "inflation", "risk", "danger", "drop", "decline", 
    "attack", "fail", "error", "unstable", "loss", "debt", "deficit", "recession", 
    "bankrupt", "protest", "strike", "violation", "harm", "damage", "corrupt",
    "unemployment", "illegal", "fraud", "scandal", "lawsuit", "unethical",
    "shortage", "stagnation", "collapse", "hostile", "embargo",

    # Student, Academic & Healthcare Sector
    "confusing", "difficult", "tough", "unorganized", "slow", "vague", "hard", 
    "useless", "rude", "harsh", "noisy", "distracted", "ignored", "irrelevant",
    "sick", "ill", "infected", "deteriorated", "unresponsive", "inaccurate",
    "plagiarism", "dropout", "fail", "incomplete", "demotivated", "defective", "broken",
    "expensive", "cheap", "waste", "slow", "buggy",
    
    # Product, Tech & Quality Sector
    "defective", "broken", "expensive", "cheap", "waste", "slow", "buggy", 
    "crash", "flawed", "overpriced", "scam", "fragile", "terrible", "noisy",
    "laggy", "vulnerable", "exposed", "outdated", "glitchy", "complex", "useless",
    "malware", "slowdown", "clunky", "unstable", "inefficient"
]

NEGATIONS = [
    "not", "no", "never", "none", "cannot", "can't", "won't", "neither", "nor",
    "didn't", "doesn't", "isn't", "aren't", "shouldn't", "wouldn't", "couldn't",
    "don't", "wasn't", "weren't", "hardly", "barely", "scarcely", "lack", "lacked",
    "without", "fails", "failed", "refused", "denied"
]

INTENSIFIERS = [
    "very", "extremely", "really", "so", "quite", "highly", "too", "super",
    "completely", "absolutely", "totally", "deeply", "fully", "incredibly",
    "exceptionally", "extraordinarily", "definitely", "certainly", "massively",
    "strongly", "vastly", "immensely", "remarkably", "wildly"
]

# System Settings
CHUNK_SIZE = 1000  # Number of records to process in one batch
DB_NAME = "analysis_results.db"