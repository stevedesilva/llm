import ollama
messages = [
    {"role": "user", "content": "Describe some the business applications of Generative AI."},
]
response = ollama.chat(model="llama3.2", messages=messages, stream=False)
print(response['message']['content'])