"""
preprocess.py - Text Preprocessing for CampusAssist

This module handles the text preprocessing pipeline:
  1. Convert text to lowercase
  2. Tokenize (split into individual words)
  3. Remove stopwords (common words like "the", "is", "a")
  4. Apply stemming (reduce words to their root form)

WHY PREPROCESS?
  Raw text contains noise — different capitalizations, filler words, and
  word variations (e.g., "libraries" vs "library") that make matching harder.
  Preprocessing normalizes the text so the AI model can focus on meaning.
"""

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

# Download required NLTK data (only needed once)
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)

# Initialize the stemmer
# PorterStemmer reduces words to their root form:
#   "running" -> "run", "libraries" -> "librari", "studies" -> "studi"
# This helps match different forms of the same word.
stemmer = PorterStemmer()

# Load English stopwords
# Stopwords are common words that carry little meaning on their own:
#   "the", "is", "at", "which", "on", etc.
# Removing them lets the model focus on the important/content words.
stop_words = set(stopwords.words("english"))

# NOTE: We initially considered keeping question words (where, when, how, what)
# since they seem meaningful. However, these words appear across almost every
# intent ("Where is the library?", "What are the fees?", "How to apply?")
# so they don't actually help distinguish between intents. Removing them
# lets the model focus on the truly distinctive content words like
# "library", "hostel", "admission", etc.

# Also add common filler verbs that appear across many intents.
# "Tell me about placements" and "Tell me a joke" both contain "tell" —
# removing it forces the model to compare "placement" vs "joke" instead.
EXTRA_STOPWORDS = {"tell", "know", "give", "please", "want", "need",
                   "find", "get", "say", "like", "also", "could", "would"}
stop_words = stop_words | EXTRA_STOPWORDS


def preprocess_text(text):
    """
    Preprocess a text string for NLP analysis.

    Steps:
      1. Lowercase the text
      2. Remove punctuation and special characters
      3. Tokenize into words
      4. Remove stopwords (except useful question words)
      5. Stem each word to its root form

    Args:
        text (str): The raw input text.

    Returns:
        str: The preprocessed text as a single string.

    Example:
        >>> preprocess_text("Where is the college library?")
        'where colleg librari'
    """
    if not text or not isinstance(text, str):
        return ""

    # Step 1: Convert to lowercase
    # "Where Is The LIBRARY?" -> "where is the library?"
    text = text.lower()

    # Step 2: Remove punctuation and special characters
    # Keep only letters, numbers, and spaces
    # "where is the library?" -> "where is the library"
    text = re.sub(r"[^a-z0-9\s]", "", text)

    # Step 3: Tokenize — split text into individual words
    # "where is the library" -> ["where", "is", "the", "library"]
    tokens = word_tokenize(text)

    # Step 4 & 5: Remove stopwords and apply stemming
    # ["where", "is", "the", "library"]
    #   -> remove "is", "the" (stopwords)
    #   -> stem "library" to "librari", keep "where"
    #   -> ["where", "librari"]
    processed_tokens = []
    for token in tokens:
        if token not in stop_words:
            stemmed = stemmer.stem(token)
            processed_tokens.append(stemmed)

    # Join tokens back into a single string (required for TF-IDF input)
    return " ".join(processed_tokens)
