import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")

openai = OpenAI()

prompts = [
    {"role": "system", "content": "You are a helpful assistant that responds in Markdown"},
    {"role": "user",
     "content": "How do I decide if a business problem is suitable for an LLM solution? Please respond in Markdown."}
]

stream = openai.chat.completions.create(
    model='gpt-4o-mini',
    messages=prompts,
    temperature=0.7,
    stream=True
)


reply = ""
for chunk in stream:
    content = chunk.choices[0].delta.content or ''
    content = content.replace("```", "").replace("markdown", "")
    reply += content
    print(content, end='', flush=True)  # Print the content in real-time


