import os
import string

from dotenv import load_dotenv
from openai import OpenAI
import anthropic

import gradio as gr

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

def shout(message):
    print(f"Input: {message}")
    return message.upper()


print(shout("what is today's date"))

# normal launch
# gr.Interface(fn=shout,inputs="textbox", outputs="textbox", flagging_mode="never").launch()

# launch in browser
# gr.Interface(fn=shout,inputs="textbox", outputs="textbox", flagging_mode="never").launch(inbrowser=True)

# share public link
# gr.Interface(fn=shout,inputs="textbox", outputs="textbox", flagging_mode="never").launch(share=True)

# Define this variable and then pass js=force_dark_mode when creating the Interface
# Inputs and Outputs
print("Dark mode\n")
force_dark_mode = """
function refresh() {
    const url = new URL(window.location);
    if (url.searchParams.get('__theme') !== 'dark') {
        url.searchParams.set('__theme', 'dark');
        window.location.href = url.href;
    }
}
"""
# gr.Interface(fn=shout, inputs="textbox", outputs="textbox", flagging_mode="never", js=force_dark_mode).launch()

# Inputs and Outputs
print("Inputs and Outputs\n")
view = gr.Interface(
    fn=shout,
    inputs=[gr.Textbox(label="Your message:", lines=6)],
    outputs=[gr.Textbox(label="Response:", lines=8)],
    flagging_mode="never"
)
view.launch()

