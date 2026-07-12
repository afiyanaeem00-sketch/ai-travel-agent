# ✈️ AI Travel Planning Agent

A multi-agent AI system that takes your **origin and destination**, researches the internet in real-time, and produces a complete travel plan with **both budget and mid-range options** — including transport, hotels, hostels, food, and practical tips.

Access here - https://ai-travel-agent-afiyanaeem-00.streamlit.app/

---

## What It Does

You enter:
```
Origin:      Delhi, India
Destination: Tokyo, Japan
```

It gives you:

```
🟢 Budget Plan     — estimated total cost, cheapest options
🔵 Mid-Range Plan  — estimated total cost, comfortable options
🚌 Transport       — flights, trains, buses + prices + booking links
🏨 Accommodation   — hostels + hotels with prices + booking links
🍜 Food            — street food + restaurants with prices
📋 Tips            — visa, currency, safety, best time to visit
```

Report saved as a `.md` file in `travel_reports/`.

---

## Architecture

```
User Input (origin + destination)
          ↓
    Coordinator
    /          \
Researcher    Planner
(Agent 1)     (Agent 2)
    ↓               ↓
web_search      create_report
scrape_webpage  save_section
save_section
          ↓
  travel_reports/trip_*.md
```

| Agent | Role | Tools |
|---|---|---|
| **Researcher** | Searches web, scrapes pages, collects all travel data | `web_search`, `scrape_webpage`, `save_section` |
| **Planner** | Organizes into budget/mid-range, creates final report | `create_travel_report`, `save_section` |
| **Coordinator** | Orchestrates both agents, handles user input | — |

---

## Setup

### 1. Clone & install

```bash
git clone https://github.com/YOUR_USERNAME/ai-travel-agent.git
cd ai-travel-agent
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Get free API keys

**Gemini API** (Google — free):
1. Go to https://aistudio.google.com/app/apikey
2. Create API key (starts with `AIza...`)

**Tavily API** (web search — free tier: 1000 searches/month):
1. Go to https://tavily.com
2. Sign up → copy API key (starts with `tvly-...`)

### 3. Set keys

```bash
# Mac/Linux
export GOOGLE_API_KEY='AIza-your-key-here'
export TAVILY_API_KEY='tvly-your-key-here'

# Windows (PowerShell)
$env:GOOGLE_API_KEY='AIza-your-key-here'
$env:TAVILY_API_KEY='tvly-your-key-here'
```

### 4. Run

```bash
python coordinator.py
```

---

## Example

```
📍 Your location: Delhi, India
🎯 Destination:   Bangkok, Thailand

[Researcher Agent searches 15+ queries across flights, hotels, food, visa...]
[Planner Agent organizes into budget + mid-range plan...]

═══════════════════════════════════════════
  📄 YOUR TRAVEL PLAN
═══════════════════════════════════════════

# ✈️ Travel Plan: Delhi, India → Bangkok, Thailand

## 💰 Quick Pick: Which Plan Suits You?

### 🟢 Budget Plan
- Flight: IndiGo/AirAsia via Kuala Lumpur, ~₹12,000-18,000 return
- Hostel: Lub d Bangkok Silom — $12/night (Hostelworld)
- Food: ~$5-8/day street food
- Estimated 7-day trip total: ~₹25,000-35,000

### 🔵 Mid-Range Plan
- Flight: Thai Airways direct, ~₹28,000-40,000 return
- Hotel: Ibis Bangkok Siam — $45/night (Booking.com)
- Food: ~$20-30/day restaurants
- Estimated 7-day trip total: ~₹60,000-80,000

## 🚌 Transport Options
...

## 🏨 Accommodation
...

Report saved to: travel_reports/trip_Bangkok_20250105_1423.md
```

---

## Project Structure

```
ai-travel-agent/
│
├── coordinator.py        # Entry point — run this
├── researcher_agent.py   # Searches + scrapes travel info
├── planner_agent.py      # Organizes into final report
├── tools.py              # All tool functions
├── requirements.txt
├── README.md
│
└── travel_reports/       # Auto-created, reports saved here
    └── trip_*.md
```

---

## Tech Stack

- **Python 3.8+**
- **Google Gemini API** — LLM + function/tool calling
- **Tavily API** — real-time web search
- **BeautifulSoup4** — webpage scraping
- **Requests** — HTTP calls

---

## Concepts Demonstrated

- ✅ Multi-agent orchestration (Coordinator → Researcher → Planner)
- ✅ Tool/function calling with Gemini API
- ✅ Real-time web search and scraping
- ✅ Autonomous decision making (agent decides what to search)
- ✅ Structured report generation

---

## Future Improvements

- [ ] Add a Critic Agent that validates prices and flags outdated info
- [ ] Add currency converter tool (live exchange rates)
- [ ] Generate PDF reports
- [ ] Build Streamlit web interface
- [ ] Add Google Flights / Skyscanner API integration

---

## License

MIT
