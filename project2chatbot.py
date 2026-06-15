# ============================================================
#  chatbot.py  —  Simple Rule-Based Chatbot
#  Author  : RuleBot Project
#  Language: Python 3
#  Run with: python chatbot.py
# ============================================================

import random   # Used to pick a random response from a list
import re       # Used for pattern matching on user input
import datetime # Used to add timestamps to log entries

# ============================================================
#  SECTION 1: INTENTS
#  Each intent has:
#    - "patterns"  : keywords/phrases we look for in user input
#    - "responses" : possible replies the bot can give (random pick)
# ============================================================

INTENTS = [
    {
        "intent": "greeting",
        "patterns": [
            "hello", "hi", "hey", "good morning",
            "good afternoon", "good evening", "howdy", "greetings"
        ],
        "responses": [
            "Hello! Welcome! How can I help you today? 😊",
            "Hi there! Great to see you. What can I do for you?",
            "Hey! I'm RuleBot. Feel free to ask me anything!",
            "Good day! How may I assist you?"
        ]
    },
    {
        "intent": "farewell",
        "patterns": [
            "bye", "goodbye", "see you", "take care",
            "farewell", "later", "see ya", "good night"
        ],
        "responses": [
            "Goodbye! Have a wonderful day! 👋",
            "See you later! Take care!",
            "Bye! It was great chatting with you!",
            "Farewell! Come back anytime you have questions!"
        ]
    },
    {
        "intent": "help",
        "patterns": [
            "help", "what can you do", "assist", "support",
            "how do you work", "what do you know", "capabilities"
        ],
        "responses": [
            "I can help you with:\n"
            "  📌 Answering questions about AI & technology\n"
            "  📌 General conversation and small talk\n"
            "  📌 Explaining concepts like ML, NLP, and more!\n"
            "Just type your question and I'll do my best!",

            "Great question! I'm a rule-based chatbot. I can:\n"
            "  ✅ Answer AI & tech questions\n"
            "  ✅ Have a friendly conversation\n"
            "  ✅ Explain concepts like Python, ML, Deep Learning\n"
            "Try asking me something!",
        ]
    },
    {
        "intent": "small_talk",
        "patterns": [
            "how are you", "what's up", "how do you feel",
            "are you okay", "how is it going", "you good",
            "what are you doing", "hows life"
        ],
        "responses": [
            "I'm just a bot, but I'm doing absolutely great! 🤖",
            "All systems running smoothly, thanks for asking!",
            "Feeling wonderful! Ready to answer your questions!",
            "I'm fantastic! Every conversation makes me better! 😄"
        ]
    },
    {
        "intent": "about_bot",
        "patterns": [
            "who are you", "what are you", "your name",
            "tell me about yourself", "introduce yourself",
            "are you a robot", "are you human", "what is rulebot"
        ],
        "responses": [
            "I'm RuleBot 🤖 — a simple rule-based chatbot built with Python!\n"
            "I use pattern matching to understand what you say and\n"
            "a knowledge base to answer your questions.",

            "My name is RuleBot! I was created using pure Python\n"
            "with no fancy AI libraries — just smart rules and patterns.\n"
            "I'm here to help you learn about AI and technology!",

            "I'm an AI chatbot powered by rule-based logic.\n"
            "I match your words to known patterns and fetch\n"
            "answers from my built-in knowledge base!"
        ]
    },
    {
        "intent": "thanks",
        "patterns": [
            "thank you", "thanks", "appreciate it",
            "cheers", "that helped", "great answer",
            "well done", "awesome", "perfect"
        ],
        "responses": [
            "You're welcome! Happy to help anytime! 😊",
            "Glad I could help! Feel free to ask more questions.",
            "Anytime! That's what I'm here for! 🤖",
            "No problem at all! Keep the questions coming!"
        ]
    },
    {
        "intent": "joke",
        "patterns": [
            "tell me a joke", "joke", "make me laugh",
            "say something funny", "humor me"
        ],
        "responses": [
            "Why do programmers prefer dark mode?\n"
            "Because light attracts bugs! 🐛😄",

            "Why did the AI go to school?\n"
            "To improve its deep learning! 🎓🤖",

            "How many programmers does it take to change a lightbulb?\n"
            "None — that's a hardware problem! 💡😂"
        ]
    }
]


# ============================================================
#  SECTION 2: KNOWLEDGE BASE
#  A dictionary where:
#    - Key   = keyword to look for in user input
#    - Value = the answer the bot will give
# ============================================================

KNOWLEDGE_BASE = {
    "artificial intelligence":
        "🤖 Artificial Intelligence (AI) is the simulation of human\n"
        "   intelligence by machines. AI systems can perform tasks like\n"
        "   learning, reasoning, problem-solving, and understanding language.",

    "machine learning":
        "📊 Machine Learning (ML) is a branch of AI where systems\n"
        "   automatically learn and improve from experience (data)\n"
        "   without being explicitly programmed for every task.",

    "deep learning":
        "🧠 Deep Learning is a subset of Machine Learning that uses\n"
        "   Neural Networks with many layers (hence 'deep') to model\n"
        "   and learn complex patterns in large amounts of data.",

    "neural network":
        "🕸️  A Neural Network is a computing model inspired by the\n"
        "   human brain. It is made up of layers of connected 'nodes'\n"
        "   (neurons) that process information and learn from data.",

    "python":
        "🐍 Python is a popular, beginner-friendly programming language.\n"
        "   It is widely used in AI, data science, web development,\n"
        "   and automation. Its simple syntax makes it great for beginners!",

    "nlp":
        "💬 Natural Language Processing (NLP) is a branch of AI that\n"
        "   helps computers understand, interpret, and generate human\n"
        "   language — like the words you type to me right now!",

    "natural language processing":
        "💬 Natural Language Processing (NLP) enables machines to\n"
        "   read, understand, and respond to human language.\n"
        "   Examples include chatbots, translation, and voice assistants.",

    "chatbot":
        "🤖 A Chatbot is a software program designed to simulate\n"
        "   conversation with humans. I am a rule-based chatbot,\n"
        "   which means I follow predefined rules to respond to you!",

    "algorithm":
        "📋 An Algorithm is a step-by-step set of instructions or rules\n"
        "   for solving a problem or completing a task.\n"
        "   Think of it like a recipe — each step leads to the final result.",

    "data science":
        "📈 Data Science is the field of using data, statistics, and\n"
        "   programming to extract insights and knowledge from large\n"
        "   datasets. It combines math, coding, and domain knowledge.",

    "computer vision":
        "👁️  Computer Vision is an AI field that trains computers to\n"
        "   interpret and understand visual information from the world,\n"
        "   such as images and videos — like facial recognition!",

    "supervised learning":
        "🎯 Supervised Learning is a type of Machine Learning where the\n"
        "   model is trained on labeled data (input + correct output).\n"
        "   Example: Teaching a model to identify cats vs. dogs.",

    "unsupervised learning":
        "🔍 Unsupervised Learning is when a model finds hidden patterns\n"
        "   in data without labeled answers. The model groups or clusters\n"
        "   data on its own — no human guidance needed!",

    "internship":
        "💼 An internship is a short-term work experience that helps\n"
        "   you apply what you've learned in real projects.\n"
        "   AI internships often involve coding, data, and model building!"
}


# ============================================================
#  SECTION 3: CONVERSATION LOG STORAGE
#  This list stores all messages in memory during the session.
# ============================================================

conversation_log = []    # Holds all chat entries for this session
message_count    = 0     # Tracks total number of messages exchanged


# ============================================================
#  FUNCTION: preprocess(user_input)
#  Purpose : Cleans up user input before pattern matching.
#            Converts to lowercase and removes punctuation.
# ============================================================

def preprocess(user_input):
    text = user_input.lower()                    # Make everything lowercase
    text = re.sub(r"[^\w\s]", "", text)          # Remove punctuation like ! ? . ,
    text = text.strip()                          # Remove extra spaces at start/end
    return text


# ============================================================
#  FUNCTION: match_intent(cleaned_input)
#  Purpose : Checks if the user's input matches any known intent.
#            Returns a random response if a match is found,
#            or None if no intent matches.
# ============================================================

def match_intent(cleaned_input):
    for intent in INTENTS:                       # Loop through each intent
        for pattern in intent["patterns"]:       # Loop through each pattern keyword
            if pattern in cleaned_input:         # Check if keyword is in user input
                return random.choice(intent["responses"])  # Return a random reply
    return None                                  # No match found


# ============================================================
#  FUNCTION: search_knowledge_base(cleaned_input)
#  Purpose : Searches the knowledge base dictionary for a keyword
#            found in the user's input.
#            Returns the answer if found, or None if not.
# ============================================================

def search_knowledge_base(cleaned_input):
    for keyword, answer in KNOWLEDGE_BASE.items():   # Loop through KB entries
        if keyword in cleaned_input:                 # Check if keyword appears in input
            return answer                            # Return the matching answer
    return None                                      # No KB match found


# ============================================================
#  FUNCTION: get_response(user_input)
#  Purpose : Master function that decides what the bot replies.
#            Priority order:
#              1. Check intents (greeting, help, etc.)
#              2. Search knowledge base (AI topics)
#              3. Return a fallback "I don't understand" message
# ============================================================

def get_response(user_input):
    cleaned = preprocess(user_input)             # Clean the input first

    # --- Step 1: Try to match an intent ---
    intent_response = match_intent(cleaned)
    if intent_response:
        return intent_response

    # --- Step 2: Try to find answer in knowledge base ---
    kb_response = search_knowledge_base(cleaned)
    if kb_response:
        return kb_response

    # --- Step 3: Fallback response ---
    fallback_responses = [
        "Hmm, I'm not sure about that. Try asking about AI, ML, or Python! 🤔",
        "I didn't quite catch that. Could you rephrase it?",
        "That's outside my knowledge for now. Ask me about AI topics!",
        "Interesting question! I don't have an answer yet. Try 'help' to see what I know."
    ]
    return random.choice(fallback_responses)


# ============================================================
#  FUNCTION: log_conversation(role, message)
#  Purpose : Saves each message to the in-memory log list AND
#            appends it to the chat_log.txt file with a timestamp.
# ============================================================

def log_conversation(role, message):
    global message_count                          # Access the global counter

    # Get current timestamp (e.g., 2026-06-13 14:35:22)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Build the log entry string
    entry = f"[{timestamp}] {role}: {message}"

    # Add to in-memory list
    conversation_log.append(entry)

    # Count only user messages to track exchanges
    if role == "You":
        message_count += 1

    # Append to chat_log.txt file (creates file if it doesn't exist)
    with open("chat_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(entry + "\n")


# ============================================================
#  FUNCTION: save_session_summary()
#  Purpose : Writes a session summary to chat_log.txt when
#            the user exits the chatbot.
# ============================================================

def save_session_summary():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    summary = (
        f"\n{'=' * 55}\n"
        f"  SESSION ENDED   : {timestamp}\n"
        f"  MESSAGES SENT   : {message_count} (by you)\n"
        f"  TOTAL LOG LINES : {len(conversation_log)}\n"
        f"{'=' * 55}\n"
    )

    # Print summary to console
    print(summary)

    # Save summary to file
    with open("chat_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(summary)


# ============================================================
#  FUNCTION: run_chatbot()
#  Purpose : The main loop that keeps the chatbot running.
#            Displays welcome banner, reads user input,
#            gets responses, logs everything, and handles exit.
# ============================================================

def run_chatbot():
    # --- Write session start header to log file ---
    session_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("chat_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"\n{'=' * 55}\n")
        log_file.write(f"  NEW SESSION STARTED: {session_start}\n")
        log_file.write(f"{'=' * 55}\n")

    # --- Display welcome banner ---
    print("=" * 55)
    print("       Welcome to RuleBot 🤖 — Your AI Assistant!      ")
    print("=" * 55)
    print("  💬 Ask me about: AI, Machine Learning, Python, NLP  ")
    print("  ❓ Type 'help' to see what I can do                 ")
    print("  🚪 Type 'quit' or 'exit' to end the session         ")
    print("=" * 55)
    print()

    # --- Main chat loop ---
    while True:

        # Get input from the user
        try:
            user_input = input("You: ").strip()
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print("\n\nRuleBot: Session interrupted. Goodbye! 👋")
            save_session_summary()
            print("✅ Chat log saved to chat_log.txt")
            break

        # --- Handle empty input ---
        if not user_input:
            print("RuleBot: Please type something! I'm here to help. 😊\n")
            continue

        # --- Handle exit commands ---
        if user_input.lower() in ["quit", "exit", "q", "bye bye"]:
            farewell = "Thank you for chatting with me! Goodbye! 👋😊"
            print(f"RuleBot: {farewell}\n")
            log_conversation("You",     user_input)
            log_conversation("RuleBot", farewell)
            save_session_summary()
            print("✅ Chat log saved to  →  chat_log.txt")
            break

        # --- Log what the user said ---
        log_conversation("You", user_input)

        # --- Generate the bot's response ---
        response = get_response(user_input)

        # --- Display the response ---
        print(f"RuleBot: {response}\n")

        # --- Log the bot's response ---
        log_conversation("RuleBot", response)


# ============================================================
#  ENTRY POINT
#  This block runs only when you execute: python chatbot.py
#  It will NOT run if this file is imported as a module.
# ============================================================

if __name__ == "__main__":
    run_chatbot()


# ============================================================
#  SAMPLE CONSOLE OUTPUT (for reference):
# ============================================================
#
#  =======================================================
#        Welcome to RuleBot 🤖 — Your AI Assistant!
#  =======================================================
#    💬 Ask me about: AI, Machine Learning, Python, NLP
#    ❓ Type 'help' to see what I can do
#    🚪 Type 'quit' or 'exit' to end the session
#  =======================================================
#
#  You: hello
#  RuleBot: Hi there! Great to see you. What can I do for you?
#
#  You: what is machine learning
#  RuleBot: 📊 Machine Learning (ML) is a branch of AI where systems
#            automatically learn and improve from experience (data)
#            without being explicitly programmed for every task.
#
#  You: tell me a joke
#  RuleBot: Why did the AI go to school?
#            To improve its deep learning! 🎓🤖
#
#  You: thank you
#  RuleBot: Glad I could help! Feel free to ask more questions.
#
#  You: quit
#  RuleBot: Thank you for chatting with me! Goodbye! 👋😊
#
#  SESSION ENDED   : 2026-06-13 14:35:44
#  MESSAGES SENT   : 4 (by you)
#  TOTAL LOG LINES : 8
#
#  ✅ Chat log saved to  →  chat_log.txt
#
# ============================================================
