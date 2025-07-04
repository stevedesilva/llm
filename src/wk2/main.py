import os
from dotenv import load_dotenv
from openai import OpenAI
import anthropic
# from IPython import display, Markdown, update_display

import google.generativeai


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

deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
if deepseek_api_key:
    print(f"DeepSeek API Key exists and begins {deepseek_api_key[:5]}")

else:
    print("DeepSeek API Key not set - please skip to the next section if you don't wish to try the DeepSeek API")

# Initialize clients
openai = OpenAI()

claude = anthropic.Anthropic()

google.generativeai.configure()

system_message = "You are an assistant that is great at telling jokes"
user_prompt = "Tell a light-hearted joke for an audience of Data Scientists"
# user_prompt = "Tell a light-hearted joke for an audience of Computer Scientists"

prompts = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": user_prompt}
]
# gpt-4o-mini
print("\n\n--- Now using gpt-4o-mini ---\n\n")
completion = openai.chat.completions.create(model='gpt-4o-mini', messages=prompts)
print(completion.choices[0].message.content)

print("\n\n--- Now using gpt-4.1-mini ---\n\n")
completion = openai.chat.completions.create(
    model='gpt-4.1-mini',
    messages=prompts,
    temperature=0.7
)
print(completion.choices[0].message.content)

print("\n\n--- Now using gpt-4.1-nano ---\n\n")
completion = openai.chat.completions.create(
    model='gpt-4.1-nano',
    messages=prompts
)
print(completion.choices[0].message.content)

print("\n\n--- Now using gpt-4.1 ---\n\n")
completion = openai.chat.completions.create(
    model='gpt-4.1',
    messages=prompts,
    temperature=0.4
)
print(completion.choices[0].message.content)

print("\n\n--- Now using o3-mini ---\n\n")
# completion = openai.chat.completions.create(
#     model='o3-mini',
#     messages=prompts
# )
completion = openai.chat.completions.create(
    model='o3-mini',
    messages=prompts
)
print(completion.choices[0].message.content)

print("\n\n--- Now using claude-3-7-sonnet-latest ---\n\n")
message = claude.messages.create(
    model="claude-3-7-sonnet-latest",
    max_tokens=200,
    temperature=0.7,
    system=system_message,
    messages=[
        {"role": "user", "content": user_prompt},
    ],
)
print(message.content[0].text)

print("\n\n--- Now using claude-3-7-sonnet-latest as stream ---\n\n")

result = claude.messages.stream(
    model="claude-3-7-sonnet-latest",
    max_tokens=200,
    temperature=0.7,
    system=system_message,
    messages=[
        {"role": "user", "content": user_prompt},
    ],
)

with result as stream:
    for text in stream:
        print(text,end='',flush=True)

print("\n\n--- Now using gemini-2.0-flash ---\n\n")
gemini = google.generativeai.GenerativeModel(
    model_name='gemini-2.0-flash',
    system_instruction=system_message
)
response = gemini.generate_content(user_prompt)
print(response.text)

#
print("\n\n--- Now using gemini-2.5-flash-preview-04-17 via OpenAI ---\n\n")
gemini_via_openai_client = OpenAI(
    api_key=google_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

response = gemini_via_openai_client.chat.completions.create(
    model="gemini-2.5-flash-preview-04-17",
    messages=prompts
)
print(response.choices[0].message.content)


print("\n\n--- Now using deepseek ---\n\n")
deepseek_via_openai_client = OpenAI(
    api_key=deepseek_api_key,
    base_url="https://api.deepseek.com"
)
response = deepseek_via_openai_client.chat.completions.create(
    model="deepseek-chat",
    messages=prompts
)
print(response.choices[0].message.content)