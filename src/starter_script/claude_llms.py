import os
from dotenv import load_dotenv
import anthropic

load_dotenv(override=True)

anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
if anthropic_api_key:
    print(f"Anthropic API Key exists and begins {anthropic_api_key[:7]}")
else:
    print("Anthropic API Key not set")

# Initialize clients
claude = anthropic.Anthropic()


claude_model = "claude-3-haiku-20240307"

claude_system = "You are an helpful assistant."










