from services.wikipedia_service import search_wikipedia


def run(task):
    queries = [
        task,
        f"{task} attractions places to visit",
        f"{task} history culture"
    ]

    results = []
    seen = set()

    for query in queries:
        try:
            for item in search_wikipedia(query):
                if item["title"] not in seen:
                    seen.add(item["title"])
                    results.append(item)
        except Exception:
            continue

    return {
        "agent": "Research Agent",
        "status": "completed",
        "source": "Wikipedia Search API",
        "queries": queries,
        "results": results[:10]
    }
