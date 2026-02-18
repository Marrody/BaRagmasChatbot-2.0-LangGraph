from duckduckgo_search import DDGS
from typing import List, Dict
from urllib.parse import urlparse


BLACKLIST_DOMAINS = [
    "youtube.com",
    "youtu.be",
    "facebook.com",
    "instagram.com",
    "tiktok.com",
    "twitter.com",
    "x.com",
    "pinterest.com",
    "yandex.ru",
    "yandex.com",
    "vimeo.com",
    "dailymotion.com",
    "reddit.com",
    "quora.com",
]

BLACKLIST_EXTENSIONS = [
    ".pdf",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".ppt",
    ".pptx",
    ".xml",
    ".json",
    ".zip",
]


def is_valid_url(url: str) -> bool:
    """Checks valid URL."""
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        path = parsed.path.lower()

        if any(bad in domain for bad in BLACKLIST_DOMAINS):
            return False

        if any(path.endswith(ext) for ext in BLACKLIST_EXTENSIONS):
            return False

        return True
    except:
        return False


def perform_web_search(query: str, max_results: int = 3) -> List[Dict[str, str]]:
    """
    Executes a DuckDuckGo search with filtering logic.
    Fetches more results than needed, filters them, and returns the top k valid ones.
    """
    print(f"🌍 Web Search: Searching for '{query}'...")
    results = []

    fetch_count = 10

    try:
        with DDGS() as ddgs:
            ddgs_gen = ddgs.text(query, max_results=fetch_count)

            for r in ddgs_gen:
                if len(results) >= max_results:
                    break

                href = r.get("href", "")

                if is_valid_url(href):
                    results.append(
                        {
                            "title": r.get("title", ""),
                            "href": href,
                            "body": r.get("body", ""),
                        }
                    )
                else:
                    print(f"🚫 Filtered blocked URL: {href}")

    except Exception as e:
        print(f"⚠️ Web Search Error: {e}")
        return []

    print(f"✅ Found {len(results)} valid results for '{query}'.")
    return results
