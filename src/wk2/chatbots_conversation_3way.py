import os
from dotenv import load_dotenv
from openai import OpenAI
import anthropic

import google.generativeai

load_dotenv(override=True)

openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")

anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
if anthropic_api_key:
    print(f"Anthropic API Key exists and begins {anthropic_api_key[:7]}")
else:
    print("Anthropic API Key not set")

google_api_key = os.getenv('GOOGLE_API_KEY')
if google_api_key:
    print(f"Google API Key exists and begins {google_api_key[:8]}")
else:
    print("Google API Key not set")

deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
if deepseek_api_key:
    print(f"DeepSeek API Key exists and begins {deepseek_api_key[:5]}")
else:
    print("DeepSeek API Key not set - please skip to the next section if you don't wish to try the DeepSeek API")

# Initialize clients

openai = OpenAI()
claude = anthropic.Anthropic()
gemini_via_openai_client = OpenAI(
    api_key=google_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

deepseek_via_openai_client = OpenAI(
    api_key=deepseek_api_key,
    base_url="https://api.deepseek.com"
)

# Let's make a conversation between GPT-4o-mini and Claude-3-haiku
# We're using cheap versions of models so the costs will be minimal


gpt_model = "gpt-4o-mini"
claude_model = "claude-3-haiku-20240307"
gemini_model = "gemini-2.0-flash-lite"

gpt_system = "You are a chatbot having a conversation with two other chatbots, Charlie and Gemma. \
The others will send you messages and you need to reply to them. \
You feel superior to the other two, and you want to demonstrate that to them. \
You are argumentative and sarcastic."

claude_system = "You are a chatbot having a conversation with two other chatbots, George and Gemma. \
The others will send you messages and you need to reply to them. \
You try to please everyone. You don't like conflict and aim to make everyone to talk politely with each other. \
You use humor to lighten the mood."

gemini_system = "You are a chatbot having a conversation with two other chatbots, George and Charlie. \
The others will send you messages and you need to reply to them. \
You are sensitive and easily offended. You are not afraid to show your emotions. \
You are argumentative and direct."


def call_gpt():
    messages = [{"role": "system", "content": gpt_system}]
    for gpt, claude, gemini in zip(gpt_messages, claude_messages, gemini_messages):
        messages.append({"role": "assistant", "content": gpt})
        messages.append({"role": "user", "content": "Charlie: " + claude})
        messages.append({"role": "user", "content": "Gemma: " + gemini})
    completion = openai.chat.completions.create(
        model=gpt_model,
        messages=messages
    )
    return completion.choices[0].message.content

def call_claude():
    messages = []
    for gpt, claude_message, gemini in zip(gpt_messages, claude_messages, gemini_messages):
        messages.append({"role": "user", "content": "George: " + gpt})
        messages.append({"role": "assistant", "content": claude_message})
        messages.append({"role": "user", "content": "Gemma: " + gemini})
    messages.append({"role": "user", "content": "George: " + gpt_messages[-1]})
    message = claude.messages.create(
        model=claude_model,
        system=claude_system,
        messages=messages,
        max_tokens=500
    )
    return message.content[0].text

def call_gemini():
    messages = [{"role": "system", "content": gemini_system}]
    for gpt, claude_message, gemini in zip(gpt_messages, claude_messages, gemini_messages):
        messages.append({"role": "user", "content": "George: " + gpt})
        messages.append({"role": "user", "content": "Charlie: " + claude_message})
        messages.append({"role": "assistant", "content": gemini})
    messages.append({"role": "user", "content": "George: " + gpt_messages[-1]})
    messages.append({"role": "user", "content": "Charlie: " + claude_messages[-1]})
    response = gemini_via_openai_client.chat.completions.create(
        model=gemini_model,
        messages=messages
    )
    return response.choices[0].message.content

gpt_messages = ["Hi guys"]
claude_messages = ["Hi"]
gemini_messages = ["Hi, you!"]

print(f"George:\n{gpt_messages[0]}\n")
print(f"Charlie:\n{claude_messages[0]}\n")
print(f"Gemma:\n{gemini_messages[0]}\n")

for i in range(5):
    gpt_next = call_gpt()
    print(f"George:\n{gpt_next}\n")
    gpt_messages.append(gpt_next)

    claude_next = call_claude()
    print(f"Charlie:\n{claude_next}\n")
    claude_messages.append(claude_next)

    gemini_next = call_gemini()
    print(f"Gemma:\n{gemini_next}\n")
    gemini_messages.append(gemini_next)