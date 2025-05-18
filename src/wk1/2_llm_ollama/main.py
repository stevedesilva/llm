# imports

import requests
from bs4 import BeautifulSoup
from IPython.display import Markdown, display

# Constants
OLLAMA_API = "http://localhost:11434/api/chat"
HEADERS = {"Content-Type": "application/json"}
MODEL = "llama3.2"
