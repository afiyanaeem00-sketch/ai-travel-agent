import os, time
from datetime import datetime
import google.genai as genai

def run_planner(origin: str, destination: str, raw_findings: str, verbose: bool = True) -> str:
    def log(msg):
        if verbose:
            print(msg)

    log(f"\n  PLANNER AGENT: {origin} to {destination}")

    client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

    trimmed = raw_findings[:5000] if len(raw_findings) > 5000 else raw_findings

    prompt = f"""Write a travel plan for {origin} to {destination}.

Research:
{trimmed}

Write in this format:

## Budget Plan
- Flight: name, price, booking site
- Hostel: name, price per night, booking site
- Food: daily cost
- Total 7-day estimate

## Mid-Range Plan
- Flight: name, price, booking site
- Hotel: name, price per night, booking site
- Food: daily cost
- Total 7-day estimate

## Transport Options
List all options with prices

## Accommodation
Budget and mid-range options with prices and booking links

## Food
Street food and restaurants with prices

## Practical Tips
Visa, currency, best time, safety"""

    for attempt in range(5):
        try:
            time.sleep(15)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            report = response.text
            log("  Report generated!")
            break
        except Exception as e:
            if "429" in str(e):
                wait = 30 * (attempt + 1)
                log(f"  Rate limit — waiting {wait}s...")
                time.sleep(wait)
            else:
                log(f"  Error: {e}")
                return f"Planner failed: {e}"
    else:
        return "Planner failed after retries."

    try:
        os.makedirs("travel_reports", exist_ok=True)
        date_str = datetime.now().strftime("%Y%m%d_%H%M")
        safe_dest = "".join(c if c.isalnum() or c in "-_" else "_" for c in destination)
        filepath = f"travel_reports/trip_{safe_dest}_{date_str}.md"
        full = f"# Travel Plan: {origin} to {destination}\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n---\n\n{report}\n\n---\nPrices approximate. Verify before booking."
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(full)
        log(f"  Saved to {filepath}")
        return full
    except Exception as e:
        return report

