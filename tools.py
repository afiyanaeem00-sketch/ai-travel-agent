import os, json, requests, time
from datetime import datetime

def web_search(query: str, num_results: int = 5) -> str:
    try:
        api_key = os.environ.get("TAVILY_API_KEY")
        if not api_key:
            return json.dumps({"error": "TAVILY_API_KEY not set"})
        response = requests.post(
            "https://api.tavily.com/search",
            json={"api_key": api_key, "query": query, "num_results": num_results, "include_answer": True},
            timeout=15
        )
        data = response.json()
        results = []
        if data.get("answer"):
            results.append({"type": "summary", "content": data["answer"]})
        for r in data.get("results", []):
            results.append({"title": r.get("title",""), "url": r.get("url",""), "snippet": r.get("content","")[:400]})
        return json.dumps(results, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

def save_section(section_name: str, content: str) -> str:
    try:
        os.makedirs("travel_reports", exist_ok=True)
        with open(f"travel_reports/_section_{section_name}.txt", "w", encoding="utf-8") as f:
            f.write(content)
        return f"Saved {section_name}"
    except Exception as e:
        return f"Error: {e}"
