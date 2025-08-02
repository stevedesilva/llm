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

# Initialize clients
openai = OpenAI()


gpt_model = "gpt-4o-mini"


gpt_system = "You are an helpful assistant."











