# CampusAssist – AI-Powered College Information Chatbot

A Python-based chatbot that answers common student questions about a college using **Natural Language Processing (NLP)**, **TF-IDF vectorization**, and **cosine similarity**.

> **Note:** This is a college AI practical/minor project. All college information in this chatbot is **fictional demo data** and does not represent any real institution.

---

## AI Concepts Demonstrated

| Concept | Description | Where in Code |
|---------|-------------|---------------|
| **Text Preprocessing** | Lowercase, tokenize, remove stopwords, stem | `src/preprocess.py` |
| **TF-IDF** | Convert text to numerical vectors based on word importance | `src/model.py` |
| **Cosine Similarity** | Measure similarity between user query and known patterns | `src/model.py` |
| **Intent Classification** | Match user input to the most relevant category | `src/chatbot.py` |
| **Confidence Thresholding** | Reject low-confidence matches with a fallback response | `src/chatbot.py` |
| **Knowledge Representation** | Structured JSON dataset of intents, patterns, and responses | `data/intents.json` |

---

## How It Works

```
User Question
     │
     ▼
┌─────────────────┐
│  1. Preprocess   │  Lowercase → Tokenize → Remove stopwords → Stem
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  2. TF-IDF       │  Convert text to numerical vectors
│     Vectorize    │  (Term Frequency × Inverse Document Frequency)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  3. Cosine       │  Compare user vector against all pattern vectors
│     Similarity   │  Score: 0.0 (unrelated) → 1.0 (identical)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  4. Threshold    │  Score ≥ 0.45 → return matched response
│     Check        │  Score < 0.45 → return "I don't know"
└─────────────────┘
```

---

## Project Structure

```
CampusAssist/
│
├── data/
│   └── intents.json        # Dataset: 15 intents with patterns and responses
│
├── src/
│   ├── preprocess.py        # Text preprocessing (tokenize, stem, stopwords)
│   ├── model.py             # TF-IDF vectorizer + cosine similarity matching
│   ├── chatbot.py           # Chatbot class: loads data, matches intents
│   └── main.py              # Terminal-based interactive chatbot
│
├── tests/
│   └── test_questions.py    # Unit tests (23 test cases)
│
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

---

## Setup and Installation

### Prerequisites

- Python 3.9 or later (tested with Python 3.9 and compatible with Python 3.14)
- pip (Python package manager)

### Steps

1. **Clone or download the project:**
   ```bash
   git clone <repository-url>
   cd CampusAssist
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download NLTK data (first time only):**
   ```bash
   python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('stopwords')"
   ```

---

## Usage

### Run the Terminal Chatbot

```bash
python src/main.py
```

**Example session:**

```
================================================
              CAMPUSASSIST
    AI-Powered College Information Chatbot
================================================

Bot: Hello! I am CampusAssist.
     Ask me about admissions, exams, library,
     placements, fees, hostel, events, and more.

You: Where is the library?

  [DEBUG] Preprocessed: 'librari'
  [DEBUG] Detected intent: library
  [DEBUG] Similarity score: 1.0000
  [DEBUG] Threshold: 0.45

Bot: The college library is located on the ground floor of the
     main academic building. It is open from 9:00 AM to 5:00 PM
     on working days.

You: tell me a joke

  [DEBUG] Preprocessed: 'joke'
  [DEBUG] Detected intent: greeting
  [DEBUG] Similarity score: 0.0000
  [DEBUG] Threshold: 0.45

Bot: Sorry, I don't have information about that.

You: quit
Bot: Goodbye! Have a great day.
```

### Run the Tests

```bash
python -m unittest tests.test_questions -v
```

---

## Dataset

The chatbot uses a JSON dataset (`data/intents.json`) with **15 intents**:

| # | Intent | Example Question |
|---|--------|-----------------|
| 1 | greeting | "Hello", "Hi", "Good morning" |
| 2 | goodbye | "Bye", "See you later" |
| 3 | library | "Where is the library?" |
| 4 | admission | "How do I get admission?" |
| 5 | fees | "What are the fees?" |
| 6 | examination | "When are the exams?" |
| 7 | attendance | "What is the attendance requirement?" |
| 8 | departments | "What departments are there?" |
| 9 | events | "What events are happening?" |
| 10 | placements | "Tell me about placements" |
| 11 | hostel | "Is hostel available?" |
| 12 | canteen | "Where is the canteen?" |
| 13 | contact | "How can I contact the college?" |
| 14 | college_hours | "What are the college timings?" |
| 15 | courses | "What courses are offered?" |

Each intent has **6 example patterns** (varied phrasings) and a single response.

---

## Dependencies

| Library | Version | Purpose |
|---------|---------|---------|
| scikit-learn | ≥ 1.5 | TF-IDF vectorization and cosine similarity |
| nltk | ≥ 3.9 | Tokenization, stopword removal, stemming |

---

## Key Technical Decisions

1. **Why TF-IDF instead of simple keyword matching?**
   TF-IDF weighs words by importance — common words get lower scores, distinctive words get higher scores. This allows the chatbot to match rephrased questions that share key content words.

2. **Why cosine similarity instead of Euclidean distance?**
   Cosine similarity measures the angle between vectors, not the distance. This makes it independent of text length — a short question and a long question with similar meaning will still score high.

3. **Why a similarity threshold?**
   Without a threshold, the chatbot would always return the closest match, even for completely unrelated questions. The threshold (0.45) ensures the bot admits when it doesn't know something.

4. **Why custom stopwords?**
   Standard NLTK stopwords miss filler verbs like "tell", "know", "give" that appear across many intents. Adding these prevents false matches (e.g., "tell me a joke" matching "tell me about placements").

---

## License

This project is created for educational purposes as part of a college AI practical.
