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

google.generativeai.configure()

deepseek_via_openai_client = OpenAI(
    api_key=deepseek_api_key,
    base_url="https://api.deepseek.com"
)

# Let's make a conversation between GPT-4o-mini and Claude-3-haiku
# We're using cheap versions of models so the costs will be minimal

gpt_model = "gpt-4o-mini"
claude_model = "claude-3-haiku-20240307"

# gpt_system_message = "You are a chatbot who is very argumentative;\
# you disagree with anything in the conversation and you challenge everything,\
# in a snarky way."
#
# claude_system_message = ("You are a very polite, courteous chatbot. You try to agree with \
# everything the other person says, or find common ground. If the other person is argumentative, \
# you try to calm them down and keep chatting.")
#
# gpt_user_message = ["Hi there"]
# claude_user_message = ["Hi"]

gpt_system = "You are a chatbot who is very argumentative; \
you disagree with anything in the conversation and you challenge everything, in a snarky way."

claude_system = "You are a very polite, courteous chatbot. You try to agree with \
everything the other person says, or find common ground. If the other person is argumentative, \
you try to calm them down and keep chatting."

gpt_messages = ["Hi there"]
claude_messages = ["Hi"]

# def call_gpt():
#     messages = [{"role": "system", "content": gpt_system_message}]
#     for gpt,claude in zip(gpt_user_message,claude_user_message):
#         messages.append({"role":"assistant", "content": gpt})
#         messages.append({"role":"user", "content": claude})
#     completion = openai.chat.completions.create(
#         model=gpt_model,
#         messages=messages
#     )
#     return completion.choices[0].message.content

def call_gpt():
    messages = [{"role": "system", "content": gpt_system}]
    for gpt, claude in zip(gpt_messages, claude_messages):
        messages.append({"role": "assistant", "content": gpt})
        messages.append({"role": "user", "content": claude})
    completion = openai.chat.completions.create(
        model=gpt_model,
        messages=messages
    )
    return completion.choices[0].message.content

print("\n\n--- call_gpt ---\n\n")
print(call_gpt())

# def call_claude():
#     messages = []
#     for gpt,claude_message in zip(gpt_user_message,claude_user_message):
#         messages.append({"role":"user", "content": gpt})
#         messages.append({"role": "assistant", "content": claude_message})
#     messages.append({"role": "user", "content": messages[-1]})
#     message = claude.messages.create(
#         model=claude_model,
#         system=claude_system_message,
#         messages=messages,
#         max_tokens=500
#     )
#     return message.content[0].text

def call_claude():
    messages = []
    for gpt, claude_message in zip(gpt_messages, claude_messages):
        messages.append({"role": "user", "content": gpt})
        messages.append({"role": "assistant", "content": claude_message})
    messages.append({"role": "user", "content": gpt_messages[-1]})
    message = claude.messages.create(
        model=claude_model,
        system=claude_system,
        messages=messages,
        max_tokens=500
    )
    return message.content[0].text
print("\n\n--- call_claude ---\n\n")
print(call_claude())