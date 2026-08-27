"""
chatbot.py - CampusAssist Chatbot

This module ties together the dataset, preprocessing, and intent matching
to create a working chatbot.

It loads the intents from the JSON dataset, trains the IntentMatcher,
and provides a simple interface to get responses for user questions.
"""

import json
import os

from model import IntentMatcher, SIMILARITY_THRESHOLD


class CampusAssistBot:
    """
    The main chatbot class.

    Loads intent data, trains the matcher, and answers user questions.
    """

    def __init__(self, data_path=None, debug=True):
        """
        Initialize the chatbot.

        Args:
            data_path (str): Path to the intents.json file.
                             Defaults to ../data/intents.json relative to this file.
            debug (bool): If True, print debug info (detected intent, similarity score).
        """
        self.debug = debug

        # Determine the path to intents.json
        if data_path is None:
            # Go up one directory from src/ to find data/
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_path = os.path.join(base_dir, "data", "intents.json")

        # Load and prepare the data
        self.intents_data = self._load_intents(data_path)
        self.response_map = self._build_response_map()

        # Train the intent matcher
        self.matcher = IntentMatcher()
        patterns, labels = self._prepare_training_data()
        self.matcher.fit(patterns, labels)

    def _load_intents(self, data_path):
        """Load intents from the JSON file."""
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data["intents"]

    def _build_response_map(self):
        """
        Build a dictionary mapping each intent tag to its response.

        Example: {"library": "The college library is located...", ...}
        """
        response_map = {}
        for intent in self.intents_data:
            response_map[intent["tag"]] = intent["response"]
        return response_map

    def _prepare_training_data(self):
        """
        Flatten all intents into two parallel lists:
          - patterns: all example questions
          - labels: the intent tag for each question

        Example:
          patterns = ["Hi", "Hello", "Where is the library?", ...]
          labels   = ["greeting", "greeting", "library", ...]
        """
        patterns = []
        labels = []
        for intent in self.intents_data:
            for pattern in intent["patterns"]:
                patterns.append(pattern)
                labels.append(intent["tag"])
        return patterns, labels

    def get_response(self, user_input):
        """
        Get a response for the user's input.

        Process:
          1. Pass input to the IntentMatcher
          2. Check if similarity score meets the threshold
          3. Return the matched response or a fallback message

        Args:
            user_input (str): The user's question.

        Returns:
            str: The bot's response.
        """
        # Handle empty input
        if not user_input or not user_input.strip():
            return "Please enter a question. I can help you with college information."

        # Get the best matching intent and similarity score
        intent, score, processed = self.matcher.predict(user_input)

        # Print debug information (useful for development and viva)
        if self.debug:
            print(f"  [DEBUG] Preprocessed: '{processed}'")
            print(f"  [DEBUG] Detected intent: {intent}")
            print(f"  [DEBUG] Similarity score: {score:.4f}")
            print(f"  [DEBUG] Threshold: {SIMILARITY_THRESHOLD}")
            print()

        # Apply the confidence threshold
        # If the similarity is too low, the bot is not confident enough
        # to give a specific answer, so it returns a fallback response.
        if intent is None or score < SIMILARITY_THRESHOLD:
            return "Sorry, I don't have information about that. You can ask me about admissions, exams, library, placements, fees, hostel, and more."

        # Return the response associated with the detected intent
        return self.response_map[intent]
