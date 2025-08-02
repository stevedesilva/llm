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
gemini_via_openai_client = OpenAI(
    api_key=google_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
deepseek_via_openai_client = OpenAI(
    api_key=deepseek_api_key,
    base_url="https://api.deepseek.com"
)

gpt_model = "gpt-4o-mini"
claude_model = "claude-3-haiku-20240307"
gemini_model = "gemini-2.0-flash-lite"
deepseek_model = "deepseek-reasoner"

gpt_system = "You are an helpful assistant."
claude_system = "You are an helpful assistant."
gemini_system = "You are an helpful assistant."
deepseek_system = "You are an helpful assistant."










