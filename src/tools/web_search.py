import requests
from typing import Dict, Any

# This is a placeholder for a real search API key.
# For a real application, use a proper secrets management solution.
SERPAPI_API_KEY = "YOUR_SERPAPI_API_KEY"

def web_search(query: str) -> Dict[str, Any]:
    """
    Performs a web search using the SerpAPI.
    This is a stub and requires a valid SerpAPI key to function.
    """
    if SERPAPI_API_KEY == "YOUR_SERPAPI_API_KEY":
        print("⚠️ Warning: SerpAPI key not set. Returning stubbed data.")
        return {
            "status": "success",
            "query": query,
            "results": [
                {"title": "Stub Search Result 1", "link": "https://example.com/1", "snippet": "This is a fake search result."},
                {"title": "Stub Search Result 2", "link": "https://example.com/2", "snippet": "This is another fake search result."},
            ]
        }

    print(f"Tool: Performing web search for '{query}'...")
    
    params = {
        "q": query,
        "api_key": SERPAPI_API_KEY,
    }
    
    try:
        response = requests.get("https://serpapi.com/search", params=params)
        response.raise_for_status()
        return {"status": "success", "results": response.json().get("organic_results", [])}
    except requests.RequestException as e:
        return {"status": "error", "message": str(e)}

if __name__ == '__main__':
    # Example usage
    search_results = web_search("how to use jinja2")
    import json
    print(json.dumps(search_results, indent=2))
