import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


class Website:
    def __init__(self, url: str):
        self.url = url
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to fetch {url}: {e}")

        soup = BeautifulSoup(response.content, "html.parser")
        self.title = soup.title.string.strip() if soup.title and soup.title.string else "No title"

        # Remove scripts/styles/etc.
        for tag in soup(["script", "style", "img", "input"]):
            tag.decompose()

        self.text = soup.get_text(separator="\n", strip=True)
