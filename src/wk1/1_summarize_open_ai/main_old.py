from website import Website
from openai_utils import summarize_url

if __name__ == "__main__":
    url = "https://edwarddonner.com"
    summary = summarize_url(url)
    print("\n--- Summary ---\n")
    print(summary)