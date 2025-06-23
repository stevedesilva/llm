# imports
import os

from IPython.display import Markdown, display, update_display
from dotenv import load_dotenv
from openai import OpenAI

# constants
MODEL_GPT = 'gpt-4o-mini'
MODEL_LLAMA = 'llama3.2'
API_KEY = "ollama"
OLLAMA_API = "http://localhost:11434/v1"

# set up environment
load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

if api_key and api_key.startswith('sk-proj-') and len(api_key)>10:
    print("API key looks good so far")
else:
    print("There might be a problem with your API key? Please visit the troubleshooting notebook!")


question = """
Please explain what this code does and why:
yield from {book.get("author") for book in books if book.get("author")}
"""
system_prompt = "You are an expert software engineer who gives clear instructions to student code queries. \
Respond in markdown."

user_prompt = "Please give a detailed explanation to the following question: " + question

# prompts
# Get gpt-4o-mini to answer, with streaming
openai_mini = OpenAI()
def stream_result(user_message, system_message, selected_model, openai):
    stream = openai.chat.completions.create(
        model=selected_model,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        stream=True
    )

    response = ""
    display_handle = display(Markdown(""), display_id=True)
    for chunk in stream:
        response += chunk.choices[0].delta.content or ''
        response = response.replace("```", "").replace("markdown", "")
        update_display(Markdown(response), display_id=display_handle.display_id)



print("MODEL_GPT....")
stream_result(user_prompt,system_prompt,MODEL_GPT,openai_mini)

print("MODEL_LLAMA....")
ollama_via_openai = OpenAI(base_url=OLLAMA_API, api_key=API_KEY)
stream_result(user_prompt,system_prompt,MODEL_LLAMA,ollama_via_openai)