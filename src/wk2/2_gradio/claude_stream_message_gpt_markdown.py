import os
from http.client import responses

import requests
from typing import List
from dotenv import load_dotenv
import anthropic

import gradio as gr
from sympy import false

load_dotenv(override=True)

anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
if anthropic_api_key:
    print(f"Anthropic API Key exists and begins {anthropic_api_key[:7]}")
else:
    print("Anthropic API Key not set")

# Initialize clients
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



view = gr.Interface(
    fn=stream_claude,
    inputs=[gr.Textbox(label="Your message:")],
    outputs=[gr.Markdown(label="Response:")],
    flagging_mode="never"
)
view.launch()

