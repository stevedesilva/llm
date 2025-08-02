import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
if deepseek_api_key:
    print(f"DeepSeek API Key exists and begins {deepseek_api_key[:5]}")
else:
    print("DeepSeek API Key not set - please skip to the next section if you don't wish to try the DeepSeek API")

# Initialize clients
deepseek_via_openai_client = OpenAI(
    api_key=deepseek_api_key,
    base_url="https://api.deepseek.com"
)


deepseek_model = "deepseek-reasoner"

deepseek_system = "You are an helpful assistant."










