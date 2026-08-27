"""
model.py - TF-IDF Intent Matching Model for CampusAssist

This module implements the core AI logic:
  1. TF-IDF Vectorization — converts text into numerical vectors
  2. Cosine Similarity — measures how similar two text vectors are
  3. Intent Matching — finds the closest matching intent for a user query

KEY CONCEPTS:

  TF-IDF (Term Frequency - Inverse Document Frequency):
    A way to represent text as numbers. Each word gets a weight based on:
    - TF: How often the word appears in THIS document (higher = more important)
    - IDF: How rare the word is ACROSS ALL documents (rarer = more important)
    This means common words get low scores, while distinctive words get high scores.

  Cosine Similarity:
    Measures the angle between two vectors (not distance).
    - 1.0 = vectors point in the same direction (identical meaning)
    - 0.0 = vectors are perpendicular (completely unrelated)
    Unlike Euclidean distance, cosine similarity is not affected by text length.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from preprocess import preprocess_text

# Similarity threshold: if the best match score is below this,
# the bot says "I don't know" instead of guessing.
# After testing, 0.45 works well — low enough to catch rephrased questions,
# high enough to reject unrelated ones like "tell me a joke".
SIMILARITY_THRESHOLD = 0.45


class IntentMatcher:
    """
    Matches user input to the most similar intent using TF-IDF and cosine similarity.

    How it works:
      1. During fit(): Preprocesses all training patterns and builds a TF-IDF matrix.
      2. During predict(): Preprocesses the user's question, converts it to a TF-IDF
         vector, and computes cosine similarity against ALL training patterns.
         Returns the intent of the most similar pattern (if above threshold).
    """

    def __init__(self):
        # The TF-IDF vectorizer learns the vocabulary from training data
        # and can then transform new text into the same vector space.
        self.vectorizer = TfidfVectorizer()

        # TF-IDF matrix of all training patterns (created during fit)
        self.tfidf_matrix = None

        # Intent label for each training pattern
        # e.g., ["greeting", "greeting", "library", "library", ...]
        self.intent_labels = []

        # Original preprocessed patterns (useful for debugging)
        self.processed_patterns = []

    def fit(self, patterns, intent_labels):
        """
        Train the model on a set of patterns and their intent labels.

        This preprocesses all patterns, then builds the TF-IDF matrix.
        The matrix has one row per pattern and one column per unique word
        in the vocabulary.

        Args:
            patterns (list[str]): List of example questions/patterns.
            intent_labels (list[str]): Corresponding intent tag for each pattern.

        Example:
            patterns = ["Where is the library?", "Hi there", "Hello"]
            labels   = ["library",               "greeting", "greeting"]
            matcher.fit(patterns, labels)
        """
        # Preprocess each pattern
        self.processed_patterns = [preprocess_text(p) for p in patterns]
        self.intent_labels = intent_labels

        # Build the TF-IDF matrix from preprocessed patterns
        # Each row is a pattern, each column is a word, each cell is the TF-IDF weight
        #
        # Example (simplified):
        #                  "librari"  "where"  "hello"  "colleg"
        # Pattern 1 (lib):   0.7       0.5      0.0      0.3
        # Pattern 2 (greet): 0.0       0.0      0.9      0.0
        # Pattern 3 (greet): 0.0       0.0      0.9      0.0
        self.tfidf_matrix = self.vectorizer.fit_transform(self.processed_patterns)

    def predict(self, user_input):
        """
        Find the best matching intent for a user's input.

        Steps:
          1. Preprocess the input text
          2. Transform it into a TF-IDF vector (using the same vocabulary)
          3. Compute cosine similarity against all training patterns
          4. Find the highest similarity score
          5. Return the intent and score (thresholding is done by the caller)

        Args:
            user_input (str): The user's raw question.

        Returns:
            tuple: (best_intent, best_score, preprocessed_input)
                - best_intent (str): The tag of the most similar intent.
                - best_score (float): The cosine similarity score (0.0 to 1.0).
                - preprocessed_input (str): The preprocessed version of the input.
        """
        # Preprocess the user's input the same way we preprocessed training data
        processed_input = preprocess_text(user_input)

        # Handle empty input after preprocessing
        if not processed_input.strip():
            return None, 0.0, processed_input

        # Transform user input into a TF-IDF vector
        # This uses the SAME vocabulary learned during fit()
        # So the vector is in the same space as the training patterns
        user_vector = self.vectorizer.transform([processed_input])

        # Compute cosine similarity between user vector and ALL training patterns
        # Result shape: (1, num_patterns) — one score per training pattern
        similarities = cosine_similarity(user_vector, self.tfidf_matrix)

        # Flatten to a 1D array and find the best match
        scores = similarities[0]
        best_index = scores.argmax()
        best_score = scores[best_index]
        best_intent = self.intent_labels[best_index]

        return best_intent, float(best_score), processed_input
