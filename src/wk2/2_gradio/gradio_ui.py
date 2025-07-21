import os
import requests
from typing import List
from dotenv import load_dotenv
from openai import OpenAI
import google.generativeai
import anthropic

import gradio as gr
from sympy import false

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


# Initialize clients

openai = OpenAI()
claude = anthropic.Anthropic()
gemini_via_openai_client = OpenAI(
    api_key=google_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Let's make a conversation between GPT-4o-mini and Claude-3-haiku
# We're using cheap versions of models so the costs will be minimal


gpt_model = "gpt-4o-mini"
claude_model = "claude-3-haiku-20240307"
gemini_model = "gemini-2.0-flash-lite"

system_message = "You are are a helpful assistant"

def message_gpt(prompt):
    message = [{"role": "system", "content": system_message},
               {"role": "user", "content": prompt}]

    completion = openai.chat.completions.create(
        model=gpt_model,
        messages=message)

    return completion.choices[0].message.content

print(message_gpt("what is today's date"))

gr.Interface(fn=message_gpt,inputs="textbox", outputs="textbox", flagging_mode="never").launch(share=True)