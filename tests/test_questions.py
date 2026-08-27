"""
test_questions.py - Test Cases for CampusAssist Chatbot

Tests cover:
  1. Exact dataset questions (should match correct intent)
  2. Rephrased questions (should still match correct intent)
  3. Unknown/unrelated questions (should return fallback)
  4. Greetings and goodbyes
  5. Edge cases (empty input, gibberish)
"""

import unittest
import sys
import os

# Add the src directory to Python path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from chatbot import CampusAssistBot


class TestCampusAssistBot(unittest.TestCase):
    """Test the CampusAssist chatbot's intent detection and responses."""

    @classmethod
    def setUpClass(cls):
        """
        Initialize the chatbot once for all tests.
        debug=False so test output isn't cluttered with debug prints.
        """
        cls.bot = CampusAssistBot(debug=False)

    # ------------------------------------------------------------------
    # Helper method
    # ------------------------------------------------------------------

    def assert_intent_detected(self, user_input, expected_intent):
        """
        Helper: Verify that the chatbot matches the input to the expected intent.
        """
        intent, score, _ = self.bot.matcher.predict(user_input)
        self.assertEqual(
            intent, expected_intent,
            f"Input: '{user_input}' -> Expected intent '{expected_intent}', "
            f"got '{intent}' (score: {score:.4f})"
        )

    # ------------------------------------------------------------------
    # Test 1: Exact questions from the dataset
    # ------------------------------------------------------------------

    def test_exact_library_question(self):
        """Exact question from dataset should match 'library' intent."""
        self.assert_intent_detected("Where is the library?", "library")

    def test_exact_admission_question(self):
        """Exact question from dataset should match 'admission' intent."""
        self.assert_intent_detected("How do I get admission?", "admission")

    def test_exact_fees_question(self):
        """Exact question from dataset should match 'fees' intent."""
        self.assert_intent_detected("What are the fees?", "fees")

    def test_exact_exam_question(self):
        """Exact question from dataset should match 'examination' intent."""
        self.assert_intent_detected("When are the exams?", "examination")

    def test_exact_placement_question(self):
        """Exact question from dataset should match 'placements' intent."""
        self.assert_intent_detected("Tell me about placements", "placements")

    # ------------------------------------------------------------------
    # Test 2: Rephrased questions (not exactly in dataset)
    # ------------------------------------------------------------------

    def test_rephrased_library(self):
        """Rephrased library question should still match 'library'."""
        self.assert_intent_detected("I want to know about the library", "library")

    def test_rephrased_hostel(self):
        """Rephrased hostel question should still match 'hostel'."""
        self.assert_intent_detected("Do you have hostel rooms?", "hostel")

    def test_rephrased_canteen(self):
        """Rephrased canteen question should still match 'canteen'."""
        self.assert_intent_detected("Where do students eat lunch?", "canteen")

    def test_rephrased_college_hours(self):
        """Rephrased timing question should match 'college_hours'."""
        self.assert_intent_detected("What time does college start in the morning?", "college_hours")

    def test_rephrased_contact(self):
        """Rephrased contact question should match 'contact'."""
        self.assert_intent_detected("How do I reach the college office?", "contact")

    # ------------------------------------------------------------------
    # Test 3: Greetings and goodbyes
    # ------------------------------------------------------------------

    def test_greeting_hello(self):
        """'Hello' should match 'greeting' intent."""
        self.assert_intent_detected("Hello", "greeting")

    def test_greeting_hi(self):
        """'Hi' should match 'greeting' intent."""
        self.assert_intent_detected("Hi", "greeting")

    def test_goodbye(self):
        """'Bye' should match 'goodbye' intent."""
        self.assert_intent_detected("Bye", "goodbye")

    def test_goodbye_variation(self):
        """'See you later' should match 'goodbye' intent."""
        self.assert_intent_detected("See you later", "goodbye")

    # ------------------------------------------------------------------
    # Test 4: Unknown / unrelated questions (should return fallback)
    # ------------------------------------------------------------------

    def test_unknown_joke(self):
        """Unrelated question should return the fallback response."""
        response = self.bot.get_response("Tell me a joke")
        self.assertIn("Sorry", response)

    def test_unknown_weather(self):
        """Weather question should return fallback."""
        response = self.bot.get_response("What is the weather today?")
        self.assertIn("Sorry", response)

    def test_unknown_recipe(self):
        """Cooking question should return fallback."""
        response = self.bot.get_response("How to make pasta?")
        self.assertIn("Sorry", response)

    # ------------------------------------------------------------------
    # Test 5: Edge cases
    # ------------------------------------------------------------------

    def test_empty_input(self):
        """Empty input should return a helpful message, not crash."""
        response = self.bot.get_response("")
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)

    def test_whitespace_input(self):
        """Whitespace-only input should be handled gracefully."""
        response = self.bot.get_response("   ")
        self.assertIsInstance(response, str)

    def test_special_characters(self):
        """Input with only special characters should not crash."""
        response = self.bot.get_response("!@#$%^&*()")
        self.assertIsInstance(response, str)

    # ------------------------------------------------------------------
    # Test 6: Response content validation
    # ------------------------------------------------------------------

    def test_library_response_content(self):
        """Library response should mention 'library'."""
        response = self.bot.get_response("Where is the library?")
        self.assertIn("library", response.lower())

    def test_placement_response_content(self):
        """Placement response should mention 'placement'."""
        response = self.bot.get_response("Tell me about placements")
        self.assertIn("placement", response.lower())

    def test_greeting_response_content(self):
        """Greeting response should be welcoming."""
        response = self.bot.get_response("Hello")
        self.assertIn("Hello", response)


if __name__ == "__main__":
    unittest.main()
