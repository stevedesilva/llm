import os
from dotenv import load_dotenv
from openai import OpenAI
from website import Website

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is missing in .env")

client = OpenAI(api_key=api_key)

def build_prompt(website: Website) -> list:
    user_msg = (
        f"You are looking at a website titled '{website.title}'.\n"
        "The contents of this website are as follows. Provide a short summary in markdown. "
        "If there is news, summarize it too.\n\n"
        f"{website.text}"
    )

    return [
        {"role": "system", "content": "You are a helpful assistant that summarizes websites."},
        {"role": "user", "content": user_msg}
    ]

def summarize_url(url: str) -> str:
    try:
        site = Website(url)
        messages = build_prompt(site)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error summarizing {url}: {e}"

