import os
from dotenv import load_dotenv
from openai import OpenAI
import anthropic
# from IPython import display, Markdown, update_display

import google.generativeai


load_dotenv(override=True)

deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
if deepseek_api_key:
    print(f"DeepSeek API Key exists and begins {deepseek_api_key[:5]}")

else:
    print("DeepSeek API Key not set - please skip to the next section if you don't wish to try the DeepSeek API")


challenge = [{"role": "system", "content": "You are a helpful assistant"},
             {"role": "user", "content": "How many words are there in your answer to this prompt"}]

print("\n\n--- Now using deepseek ---\n\n")
deepseek_via_openai_client = OpenAI(
    api_key=deepseek_api_key,
    base_url="https://api.deepseek.com"
)
stream = deepseek_via_openai_client.chat.completions.create(
    model="deepseek-chat",
    messages=challenge,
    stream=True
)


# Stream the response
full_response = ""
for chunk in stream:
    if chunk.choices[0].delta.content:
        content = chunk.choices[0].delta.content
        full_response += content
        print(content, end='', flush=True)

print()  # Add newline at the end

print("\n\n--- Now using deepseek as stream ---\n\n")
challenge = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "How may words are there in your answer to this prompt?"}
]

stream = deepseek_via_openai_client.chat.completions.create(
    model="deepseek-chat",
    messages=challenge,
    stream=True
)

reply = ""
for chunk in stream:
    content = chunk.choices[0].delta.content or ''
    content = content.replace("```", "").replace("markdown", "")
    reply += content
    print(content, end='', flush=True)  # Print the content in real-time

print("\n\nNumber of words:", len(reply.split(" ")))


print("\n\n--- Now using deepseek reasoner model ---\n\n")
response = deepseek_via_openai_client.chat.completions.create(
    model="deepseek-reasoner",
    messages=challenge
)

reasoning_content = response.choices[0].message.reasoning_content
content = response.choices[0].message.content

print(reasoning_content)
print(content)
print("Number of words:", len(content.split(" ")))