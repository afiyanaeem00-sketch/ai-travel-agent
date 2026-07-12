import os, json, time
import google.genai as genai
from tools import web_search, save_section

def run_researcher(origin: str, destination: str, verbose: bool = True) -> str:
    def log(msg):
        if verbose:
            print(msg)

    log(f"\n  RESEARCHER AGENT: {origin} to {destination}")

    queries = [
        ("flights", f"cheapest flights {origin} to {destination} price airlines"),
        ("hostels", f"budget hostels {destination} price per night"),
        ("hotels",  f"mid range hotels {destination} price per night"),
        ("food",    f"street food restaurants {destination} prices"),
        ("visa",    f"visa {destination} Indian passport requirements"),
    ]

    combined = ""
    for section, query in queries:
        log(f"  Searching: {query[:55]}...")
        result = web_search(query)
        save_section(section, result)
        combined += f"\n\n--- {section.upper()} ---\n{result}"
        time.sleep(1)

    log("  Searches done. Summarizing with Gemini...")

    client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

    prompt = f"""Summarize this travel research for {origin} to {destination}.

{combined[:5000]}

Give me:
- Cheapest flight options with prices and airlines
- Budget hostel names and prices per night
- Mid-range hotel names and prices per night
- Street food and restaurant prices
- Visa requirements for Indian passport holders"""

    for attempt in range(5):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            log("  Summary done!")
            return response.text
        except Exception as e:
            if "429" in str(e):
                wait = 30 * (attempt + 1)
                log(f"  Rate limit — waiting {wait}s...")
                time.sleep(wait)
            else:
                log(f"  Error: {e}. Returning raw data.")
                return combined

    return combined
