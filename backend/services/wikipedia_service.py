import re
import requests

URL = "https://en.wikipedia.org/w/api.php"


def search_wikipedia(query, limit=5):
    response = requests.get(
        URL,
        params={
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "utf8": 1,
            "srlimit": limit
        },
        timeout=10
    )
    response.raise_for_status()

    results = []
    for item in response.json().get("query", {}).get("search", []):
        title = item.get("title", "")
        results.append({
            "title": title,
            "snippet": re.sub(r"<[^>]+>", "", item.get("snippet", "")),
            "url": "https://en.wikipedia.org/wiki/" + title.replace(" ", "_")
        })
    return results
