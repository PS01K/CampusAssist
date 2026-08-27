"""
main.py - CampusAssist Terminal Interface

Run this file to start the interactive chatbot in your terminal:
    python src/main.py
"""

from chatbot import CampusAssistBot


def print_banner():
    """Print the welcome banner."""
    print()
    print("=" * 48)
    print("              CAMPUSASSIST")
    print("    AI-Powered College Information Chatbot")
    print("=" * 48)
    print()


def main():
    """Run the interactive chatbot loop."""
    print_banner()

    # Initialize the chatbot (loads data and trains the model)
    print("Loading chatbot...")
    bot = CampusAssistBot(debug=True)
    print()

    # Welcome message
    print("Bot: Hello! I am CampusAssist.")
    print("     Ask me about admissions, exams, library,")
    print("     placements, fees, hostel, events, and more.")
    print()
    print("     Type 'quit' or 'exit' to end the conversation.")
    print("-" * 48)
    print()

    # Interactive chat loop
    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            # Handle Ctrl+C or Ctrl+D gracefully
            print("\n\nBot: Goodbye! Have a great day.\n")
            break

        # Skip empty input
        if not user_input:
            continue

        # Check for exit commands
        if user_input.lower() in ("quit", "exit"):
            print("\nBot: Goodbye! Have a great day.\n")
            break

        # Get and display the response
        response = bot.get_response(user_input)
        print(f"Bot: {response}")
        print()


if __name__ == "__main__":
    main()
