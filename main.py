from flask import Flask, render_template, request
import json
from difflib import get_close_matches

app = Flask(__name__)

def load_knowledge_base(file_path: str) -> dict:
    """Load the knowledge base from a JSON file."""
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return {"questions": []}  # Return an empty structure if file is missing
    except json.JSONDecodeError:
        print(f"Error: The file '{file_path}' is not a valid JSON.")
        return {"questions": []}  # Return an empty structure if JSON is invalid

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    """Find the closest matching question from the knowledge base."""
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    """Get the answer corresponding to the matched question."""
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None

@app.route('/', methods=['GET', 'POST'])
def main():
    user_messages = []
    bot_messages = []
    
    # Correct the path here
    knowledge_base_file = r"C:\Users\GURMEJ SINGH\Desktop\CHATBOT2\knowledge_base.json"
    knowledge_base = load_knowledge_base(knowledge_base_file)

    if request.method == 'POST':
        user_message = request.form["message"]
        
        best_match = find_best_match(user_message, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer = get_answer_for_question(best_match, knowledge_base)
            bot_message = answer if answer else "Bot: I do not know."
        else:
            bot_message = "Bot: I do not know."

        user_messages.append(user_message)
        bot_messages.append(bot_message)

    return render_template('index.html', user_messages=user_messages, bot_messages=bot_messages)

if __name__ == "__main__":
    app.run(debug=True)
