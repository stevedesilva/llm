from openai import OpenAI

MODEL = "deepseek-r1:1.5b"
API_KEY = "ollama"
OLLAMA_API = "http://localhost:11434/v1"

messages = [
    {"role": "user", "content": "Describe some the business applications of Generative AI."},
]
ollama_via_openai = OpenAI(base_url=OLLAMA_API, api_key=API_KEY)

response = ollama_via_openai.chat.completions.create(
    model=MODEL,
    messages=messages
)
print(response.choices[0].message.content)