import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')

if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")

if anthropic_api_key:
    print(f"Anthropic API Key exists and begins {anthropic_api_key[:7]}")
else:
    print("Anthropic API Key not set")

if google_api_key:
    print(f"Google API Key exists and begins {google_api_key[:8]}")
else:
    print("Google API Key not set")

openai = OpenAI()
MODEL = 'gpt-4o-mini'


def build_system_prompt(language: str, difficulty: str) -> str:
    """Construct a prompt for generating a relevant question based on language and difficulty."""
    return (
        f"You are a programming instructor.\n"
        f"Ask one {difficulty.lower()}-level question about {language}. "
        f"Make it clear, practical, and appropriate for someone at the {difficulty.lower()} level."
    )

def build_evaluation_prompt(question: str, user_answer: str) -> str:
    """Build evaluation prompt."""
    return (
        "You are a strict but fair programming tutor.\n\n"
        f"The question was:\n{question}\n\n"
        f"The student's answer is:\n{user_answer}\n\n"
        "Evaluate the answer and provide clear, constructive feedback. "
        "Give and clear example."
        "Say if it's correct, and explain why or why not."
    )

def ask_question(language: str, difficulty: str):
    """Generate a question based on language and difficulty level."""
    try:
        prompt = build_system_prompt(language, difficulty)
        response = openai.chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": prompt}]
        )
        question = response.choices[0].message.content.strip()
    except Exception as e:
        question = f"❌ Error generating question: {e}"

    messages = [{"role": "assistant", "content": question}]
    return messages, messages

def evaluate_answer(user_answer: str, chat_history: list):
    """Evaluate user's answer."""
    question = next((msg["content"] for msg in reversed(chat_history) if msg["role"] == "assistant"), None)

    if not question:
        fallback = "❗ I couldn’t find the question to evaluate. Please start over."
        updated = chat_history + [{"role": "assistant", "content": fallback}]
        yield updated, updated
        return

    try:
        eval_prompt = build_evaluation_prompt(question, user_answer)

        stream = openai.chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": eval_prompt}],
            stream=True
        )

        feedback = ""
        for chunk in stream:
            content = chunk.choices[0].delta.content or ""
            feedback += content
            updated_history = chat_history + [
                {"role": "user", "content": user_answer},
                {"role": "assistant", "content": feedback}
            ]
            yield updated_history, updated_history

    except Exception as e:
        error_msg = f"❌ Error evaluating answer: {e}"
        updated = chat_history + [{"role": "assistant", "content": error_msg}]
        yield updated, updated

# --- UI Layout ---
with gr.Blocks() as demo:
    gr.Markdown("## 🧠 Programming Tutor\n\nChoose a language and difficulty, get a question, and receive feedback on your answer.")

    state = gr.State([])  # conversation history
    chatbot = gr.Chatbot(type="messages")

    with gr.Row():
        language_dropdown = gr.Dropdown(
            choices=["Regular expressions", "Data Structures and Algorithms", "Coding Architecture", "Coding Data Patterns", "Coding Python", "Coding JavaScript", "Coding Go", "Coding Java"],
            label="📘 Question choice",
            value="Coding Java"
        )

        difficulty_dropdown = gr.Dropdown(
            choices=["Beginner", "Intermediate", "Advanced"],
            label="🎯 Difficulty",
            value="Beginner"
        )

    with gr.Row():
        ask_btn = gr.Button("🧩 Get a Question")

    user_answer = gr.Textbox(
        label="✏️ Your Answer",
        placeholder="Type your answer here and press Enter",
        lines=2
    )

    # Ask question based on language + difficulty
    ask_btn.click(
        fn=ask_question,
        inputs=[language_dropdown, difficulty_dropdown],
        outputs=[chatbot, state]
    )

    # Evaluate user answer
    user_answer.submit(
        fn=evaluate_answer,
        inputs=[user_answer, state],
        outputs=[chatbot, state]
    )

demo.launch()
