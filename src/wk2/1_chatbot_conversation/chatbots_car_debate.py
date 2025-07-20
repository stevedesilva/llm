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

system = ("You are a car expert debating the pros and cons of getting an electric or a hybrid SUV in the uk. \
The user is trying to decide which to get. \
The user travels short distances. \
The user drives 3 to 4 times per week. \
The user likes luxury SUVs. \
The user wants a second hand luxury SUVs. \
The user does not have a home charger \
The user may have access to home charger in 6 months \
The user wants a recommendation.")


def call_gpt():
    messages = [{"role": "system", "content": system}]
    for gpt_msg, claude_msg in zip(gpt_messages, claude_messages):
        messages.append({"role": "assistant", "content": gpt_msg})
        messages.append({"role": "user", "content": claude_msg})
    completion = openai.chat.completions.create(
        model=gpt_model,
        messages=messages
    )
    return completion.choices[0].message.content

def call_claude():
    messages = []
    for gpt_msg,claude_msg in zip(gpt_messages,claude_messages):
        messages.append({"role" : "user", "content": gpt_msg})
        messages.append({"role": "assistant", "content": claude_msg})
    messages.append({"role": "user", "content": gpt_messages[-1]})
    message = claude.messages.create(
        model=claude_model,
        system=system,
        messages=messages,
        max_tokens=500
    )
    return message.content[0].text


gpt_messages = ["Let's compare Land Rover Discovery Sport hybrid vs Telsa model Y "]
claude_messages = ["Sure,lets debate the pros and cons and recommend the best one"]


print(f"GPT:\n\n{gpt_messages[0]}\n")
print(f"Claude:\n\n{claude_messages[0]}\n")

for i in range(5):
    gpt_next = call_gpt()
    print(f"GPT:\n{gpt_next}\n")
    gpt_messages.append(gpt_next)

    claude_next = call_claude()
    print(f"Claude:\n{claude_next}\n")
    claude_messages.append(claude_next)
    

