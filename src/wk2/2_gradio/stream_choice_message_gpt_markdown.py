import os
from http.client import responses

import requests
from typing import List
from dotenv import load_dotenv
import anthropic
from openai import OpenAI

import gradio as gr
from sympy import false

load_dotenv(override=True)

openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")

# Initialize client
openai = OpenAI()

anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
if anthropic_api_key:
    print(f"Anthropic API Key exists and begins {anthropic_api_key[:7]}")
else:
    print("Anthropic API Key not set")

# Initialize client
claude = anthropic.Anthropic()

system_message = "You are a helpful assistant that responds in markdown"

def stream_claude(prompt):
    result = claude.messages.stream(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        temperature=0.7,
        system=system_message,
        messages=[
            {"role":"user", "content": prompt},
        ]
    )
    response = ""
    with result as stream:
        for text in stream.text_stream:
            response += text or ""
            yield response



# view = gr.Interface(
#     fn=stream_claude,
#     inputs=[gr.Textbox(label="Your message:")],
#     outputs=[gr.Markdown(label="Response:")],
#     flagging_mode="never"
# )
# view.launch()

def stream_gpt(prompt):
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
      ]
    stream = openai.chat.completions.create(
        model='gpt-4o-mini',
        messages=messages,
        stream=True
    )
    result = ""
    for chunk in stream:
        result += chunk.choices[0].delta.content or ""
        yield result


# view = gr.Interface(
#     fn=stream_gpt,
#     inputs=[gr.Textbox(label="Your message:")],
#     outputs=[gr.Markdown(label="Response:")],
#     flagging_mode="never"
# )
# view.launch()

def stream_model(prompt, model):
    if model == 'GPT':
        result = stream_gpt(prompt)
    elif model == "Claude":
        result = stream_claude(prompt)
    else:
        raise ValueError("unknown model")
    yield from result

view = gr.Interface(
    fn=stream_model,
    inputs=[gr.Textbox(label="Your message:"),gr.Dropdown(['GPT','Claude'],label="Select models", value='GPT')],
    outputs=[gr.Markdown(label="Response:")],
    flagging_mode="never"
)
view.launch()
