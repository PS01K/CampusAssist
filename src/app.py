"""
app.py - Simple Web Interface for CampusAssist

A minimal Flask app that provides a browser-based chat UI.
This is an optional addition to the terminal chatbot.

Run with:
    python src/app.py

Then open http://localhost:5000 in your browser.
"""

import sys
import os

# Add src directory to path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify, render_template_string
from chatbot import CampusAssistBot

app = Flask(__name__)

# Initialize chatbot once when the server starts
bot = CampusAssistBot(debug=False)

# ---------------------------------------------------------------------------
# HTML template with embedded CSS and JavaScript (single-file approach)
# ---------------------------------------------------------------------------

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CampusAssist – AI College Chatbot</title>
    <meta name="description" content="CampusAssist is an AI-powered chatbot that answers student questions about college admissions, exams, library, placements, and more.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        :root {
            --bg-primary: #0f1117;
            --bg-secondary: #1a1d27;
            --bg-chat: #141620;
            --bg-user-msg: #3b82f6;
            --bg-bot-msg: #1e2235;
            --text-primary: #e8eaed;
            --text-secondary: #9aa0b0;
            --text-on-accent: #ffffff;
            --accent: #3b82f6;
            --accent-hover: #2563eb;
            --border: #2a2d3a;
            --shadow: 0 4px 24px rgba(0, 0, 0, 0.3);
            --radius: 12px;
            --radius-msg: 18px;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }

        /* ---- Chat Container ---- */
        .chat-container {
            width: 100%;
            max-width: 520px;
            height: 92vh;
            display: flex;
            flex-direction: column;
            background: var(--bg-secondary);
            border-radius: 20px;
            border: 1px solid var(--border);
            box-shadow: var(--shadow);
            overflow: hidden;
        }

        /* ---- Header ---- */
        .chat-header {
            padding: 20px 24px;
            background: linear-gradient(135deg, #1e2235 0%, #252a3a 100%);
            border-bottom: 1px solid var(--border);
            text-align: center;
        }

        .chat-header h1 {
            font-size: 1.2rem;
            font-weight: 700;
            letter-spacing: 1px;
            background: linear-gradient(135deg, #60a5fa, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .chat-header p {
            font-size: 0.78rem;
            color: var(--text-secondary);
            margin-top: 4px;
        }

        /* ---- Status indicator ---- */
        .status-dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            background: #22c55e;
            border-radius: 50%;
            margin-right: 6px;
            animation: pulse-dot 2s ease-in-out infinite;
        }

        @keyframes pulse-dot {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.4; }
        }

        /* ---- Messages Area ---- */
        .chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 20px 16px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            background: var(--bg-chat);
            scroll-behavior: smooth;
        }

        .chat-messages::-webkit-scrollbar {
            width: 5px;
        }

        .chat-messages::-webkit-scrollbar-track {
            background: transparent;
        }

        .chat-messages::-webkit-scrollbar-thumb {
            background: var(--border);
            border-radius: 4px;
        }

        /* ---- Message Bubbles ---- */
        .message {
            max-width: 82%;
            padding: 12px 16px;
            border-radius: var(--radius-msg);
            font-size: 0.9rem;
            line-height: 1.55;
            animation: fadeSlideIn 0.3s ease-out;
            word-wrap: break-word;
        }

        @keyframes fadeSlideIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .message.bot {
            align-self: flex-start;
            background: var(--bg-bot-msg);
            color: var(--text-primary);
            border-bottom-left-radius: 6px;
        }

        .message.user {
            align-self: flex-end;
            background: var(--bg-user-msg);
            color: var(--text-on-accent);
            border-bottom-right-radius: 6px;
        }

        .message-label {
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 4px;
            opacity: 0.7;
        }

        .message.bot .message-label { color: #a78bfa; }
        .message.user .message-label { color: rgba(255, 255, 255, 0.7); }

        /* ---- Typing Indicator ---- */
        .typing-indicator {
            display: none;
            align-self: flex-start;
            padding: 12px 20px;
            background: var(--bg-bot-msg);
            border-radius: var(--radius-msg);
            border-bottom-left-radius: 6px;
        }

        .typing-indicator span {
            display: inline-block;
            width: 8px;
            height: 8px;
            background: var(--text-secondary);
            border-radius: 50%;
            margin: 0 2px;
            animation: typingBounce 1.2s ease-in-out infinite;
        }

        .typing-indicator span:nth-child(2) { animation-delay: 0.15s; }
        .typing-indicator span:nth-child(3) { animation-delay: 0.3s; }

        @keyframes typingBounce {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-6px); }
        }

        /* ---- Input Area ---- */
        .chat-input-area {
            padding: 16px;
            border-top: 1px solid var(--border);
            background: var(--bg-secondary);
        }

        .chat-input-wrapper {
            display: flex;
            gap: 10px;
            align-items: center;
        }

        #user-input {
            flex: 1;
            padding: 12px 18px;
            border: 1px solid var(--border);
            border-radius: 24px;
            background: var(--bg-chat);
            color: var(--text-primary);
            font-family: inherit;
            font-size: 0.9rem;
            outline: none;
            transition: border-color 0.2s;
        }

        #user-input:focus {
            border-color: var(--accent);
        }

        #user-input::placeholder {
            color: var(--text-secondary);
        }

        #send-btn {
            width: 44px;
            height: 44px;
            border: none;
            border-radius: 50%;
            background: var(--accent);
            color: white;
            font-size: 1.2rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background 0.2s, transform 0.15s;
            flex-shrink: 0;
        }

        #send-btn:hover {
            background: var(--accent-hover);
            transform: scale(1.05);
        }

        #send-btn:active {
            transform: scale(0.95);
        }

        /* ---- Quick Action Chips ---- */
        .quick-actions {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            padding: 0 16px 12px;
            background: var(--bg-chat);
        }

        .chip {
            padding: 6px 14px;
            border: 1px solid var(--border);
            border-radius: 20px;
            background: transparent;
            color: var(--text-secondary);
            font-family: inherit;
            font-size: 0.75rem;
            cursor: pointer;
            transition: all 0.2s;
        }

        .chip:hover {
            border-color: var(--accent);
            color: var(--accent);
            background: rgba(59, 130, 246, 0.08);
        }

        /* ---- Responsive ---- */
        @media (max-width: 560px) {
            .chat-container {
                max-width: 100%;
                height: 100vh;
                border-radius: 0;
                border: none;
            }
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <!-- Header -->
        <div class="chat-header">
            <h1>CAMPUS-ASSIST</h1>
            <p><span class="status-dot"></span>AI-Powered College Information Chatbot</p>
        </div>

        <!-- Messages -->
        <div class="chat-messages" id="chat-messages">
            <div class="message bot">
                <div class="message-label">CampusAssist</div>
                Hello! I am CampusAssist, your college information assistant. Ask me about admissions, exams, library, placements, fees, hostel, events, and more.
            </div>
        </div>

        <!-- Quick Actions -->
        <div class="quick-actions" id="quick-actions">
            <button class="chip" onclick="sendQuickAction(this)">Library</button>
            <button class="chip" onclick="sendQuickAction(this)">Admissions</button>
            <button class="chip" onclick="sendQuickAction(this)">Placements</button>
            <button class="chip" onclick="sendQuickAction(this)">Fees</button>
            <button class="chip" onclick="sendQuickAction(this)">Hostel</button>
            <button class="chip" onclick="sendQuickAction(this)">Exams</button>
        </div>

        <!-- Input -->
        <div class="chat-input-area">
            <div class="chat-input-wrapper">
                <input
                    type="text"
                    id="user-input"
                    placeholder="Ask a question..."
                    autocomplete="off"
                >
                <button id="send-btn" onclick="sendMessage()" title="Send">
                    &#10148;
                </button>
            </div>
        </div>
    </div>

    <script>
        const messagesDiv = document.getElementById('chat-messages');
        const userInput = document.getElementById('user-input');
        const quickActions = document.getElementById('quick-actions');

        // Send on Enter key
        userInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') sendMessage();
        });

        // Focus input on load
        userInput.focus();

        function addMessage(text, sender) {
            const msg = document.createElement('div');
            msg.className = 'message ' + sender;

            const label = document.createElement('div');
            label.className = 'message-label';
            label.textContent = sender === 'bot' ? 'CampusAssist' : 'You';

            msg.appendChild(label);
            msg.appendChild(document.createTextNode(text));
            messagesDiv.appendChild(msg);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }

        function showTyping() {
            const indicator = document.createElement('div');
            indicator.className = 'typing-indicator';
            indicator.id = 'typing';
            indicator.style.display = 'flex';
            indicator.innerHTML = '<span></span><span></span><span></span>';
            messagesDiv.appendChild(indicator);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }

        function hideTyping() {
            const indicator = document.getElementById('typing');
            if (indicator) indicator.remove();
        }

        function sendQuickAction(btn) {
            userInput.value = btn.textContent;
            sendMessage();
        }

        async function sendMessage() {
            const text = userInput.value.trim();
            if (!text) return;

            // Add user message
            addMessage(text, 'user');
            userInput.value = '';

            // Hide quick actions after first message
            quickActions.style.display = 'none';

            // Show typing indicator
            showTyping();

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text })
                });
                const data = await response.json();

                // Small delay for natural feel
                setTimeout(() => {
                    hideTyping();
                    addMessage(data.response, 'bot');
                }, 400);
            } catch (err) {
                hideTyping();
                addMessage('Sorry, something went wrong. Please try again.', 'bot');
            }
        }
    </script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def home():
    """Serve the chat interface."""
    return render_template_string(HTML_TEMPLATE)


@app.route("/chat", methods=["POST"])
def chat():
    """
    API endpoint: receive a user message and return the bot's response.

    Request:  { "message": "Where is the library?" }
    Response: { "response": "The college library is...", "intent": "library", "score": 0.95 }
    """
    data = request.get_json()
    user_message = data.get("message", "")

    # Get intent and score for the response (useful for debugging)
    intent, score, _ = bot.matcher.predict(user_message)
    response = bot.get_response(user_message)

    return jsonify({
        "response": response,
        "intent": intent,
        "score": round(score, 4)
    })


if __name__ == "__main__":
    print()
    print("=" * 48)
    print("  CampusAssist Web UI")
    print("  Open http://localhost:5000 in your browser")
    print("=" * 48)
    print()
    app.run(debug=False, port=5000)
