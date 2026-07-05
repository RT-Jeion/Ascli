from ddgs import DDGS


def web_search(query: str, max_results: int = 10):
    """Searches the web for the given query and returns a text summary of results."""

    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=int(max_results))]

        if not results:
            return "No relevant web results found."

        formatted_results = []
        for r in results:
            formatted_results.append(
                f"Title: {r['title']}\nURL: {r['href']}\nSnippet: {r['body']}\n"
            )
        return formatted_results

    except Exception as e:
        return f"Search failed: {str(e)}"


if __name__ == "__main__":
    result = web_search(query="Adlof Hitler", max_results=100)
    for i, r in enumerate(result):
        print(f"Result no.{i}")
        print(r)

