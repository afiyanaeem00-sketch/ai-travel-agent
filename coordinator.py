import os, sys, time
import google.genai as genai
from researcher_agent import run_researcher
from planner_agent import run_planner

def setup():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("ERROR: GOOGLE_API_KEY not set!")
        print("Run: set GOOGLE_API_KEY=your-key")
        sys.exit(1)
    tavily = os.environ.get("TAVILY_API_KEY")
    if not tavily:
        print("WARNING: TAVILY_API_KEY not set — search won't work!")
    print("APIs configured.")

def plan_trip(origin, destination, verbose=True):
    print(f"\n{'='*60}")
    print(f"  AI TRAVEL AGENT")
    print(f"  {origin} to {destination}")
    print(f"{'='*60}")

    print("\n  PHASE 1/2: Researcher Agent...")
    t1 = time.time()
    findings = run_researcher(origin, destination, verbose)
    print(f"  Research done ({round(time.time()-t1, 1)}s) — {len(findings)} chars")

    print("\n  PHASE 2/2: Planner Agent...")
    t2 = time.time()
    report = run_planner(origin, destination, findings, verbose)
    print(f"  Planning done ({round(time.time()-t2, 1)}s)")

    return report

def main():
    setup()
    print("\n  AI TRAVEL PLANNING AGENT")
    print("  Enter origin and destination to get a full travel plan.")
    print("  Type quit to exit.\n")

    while True:
        try:
            origin = input("Your location: ").strip()
            if origin.lower() in ["quit","exit"]: break
            if not origin: continue

            destination = input("Destination: ").strip()
            if not destination: continue

            verbose = input("Show logs? (y/n): ").strip().lower() != "n"

            report = plan_trip(origin, destination, verbose)

            print(f"\n{'='*60}")
            print("  YOUR TRAVEL PLAN")
            print(f"{'='*60}\n")
            print(report)
            print(f"\nReport saved to travel_reports/ folder.")

            again = input("\nPlan another trip? (y/n): ").strip().lower()
            if again != "y":
                break

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
