import os
from dotenv import load_dotenv
from openai import OpenAI
import anthropic

import google.generativeai

load_dotenv(override=True)


google_api_key = os.getenv('GOOGLE_API_KEY')
if google_api_key:
    print(f"Google API Key exists and begins {google_api_key[:8]}")
else:
    print("Google API Key not set")


gemini_via_openai_client = OpenAI(
    api_key=google_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

gemini_model = "gemini-2.0-flash-lite"
gemini_system = "You are an helpful assistant."










