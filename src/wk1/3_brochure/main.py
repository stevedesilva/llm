import os
import requests
import json
from typing import List
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display, update_display
from openai import OpenAI, api_key

# Load environment variables
load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

if api_key and api_key.startswith("sk-proj-"):
    print("API key found and looks good so far!")
else:
    print("❌ Invalid API key. Please check your .env file or the troubleshooting notebook.")

# Define the model and API endpoint
MODEL = 'gpt-4o-mini'
openai = OpenAI()
