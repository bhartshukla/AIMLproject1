# AI Agent Hub

A single Streamlit app that brings together five Agno agents in one place. Every agent uses one free provider - Groq - and nothing else.

| Page | Agent | Model | Tools |
|---|---|---|---|
| Travel Agent | Travel safety / advisory Q&A | Groq `openai/gpt-oss-120b` (free) | DuckDuckGo web search |
| Stock Analyst | Stock prices, fundamentals, recommendations | Groq `openai/gpt-oss-120b` (free) | YFinance + DuckDuckGo |
| Memory Chat | Remembers facts about each user | Groq `openai/gpt-oss-120b` (free) | SQLite (`agno_memory.db`) |
| Translator Team | 3 agents (EN/ZH/HI) answer together | Groq `openai/gpt-oss-120b` (free) | Agno `Team` |
| YouTube Analyzer | Timestamped, structured video breakdown | Groq `openai/gpt-oss-120b` (free) | `YouTubeTools` |

## Project structure

```
agno-agent-hub/
├── app.py                       # Landing page
├── agents/
│   ├── travel_agent.py
│   ├── stock_agent.py
│   ├── memory_agent.py
│   ├── translator_team.py
│   └── youtube_agent.py
├── pages/                       # Streamlit auto-discovers these as sidebar pages
│   ├── 1_Travel_Agent.py
│   ├── 2_Stock_Analyst.py
│   ├── 3_Memory_Chat.py
│   ├── 4_Translator_Team.py
│   └── 5_YouTube_Analyzer.py
├── requirements.txt
└── .env.example
```

## Setup

1. Virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Environment variables - copy `.env.example` to `.env` and fill in your key:
   ```bash
   cp .env.example .env
   ```
   - `GROQ_API_KEY` - free, needed for all 5 agents. Sign up at https://console.groq.com/keys - no credit card required.

4. Run the app:
   ```bash
   streamlit run app.py
   ```

5. Open `http://localhost:8501` in your browser - pick any agent from the sidebar.

## Notes

- Each agent lives in its own file under `agents/`, so it can be imported and tested independently of the Streamlit UI.
- The Memory Chat agent creates an `agno_memory.db` (SQLite) file in the project root on first use - it stores memories separately per `user_id`.
- Every single `Agent`/`Team` instance in this project (8 total across 5 files) explicitly sets `model=Groq(id="openai/gpt-oss-120b")` - nothing silently falls back to a different provider, so one `GROQ_API_KEY` is all you need.
- Page filenames use plain text only (no emoji) to avoid encoding/mojibake issues in some Windows terminals and browsers.

## Troubleshooting

- **`ModuleNotFoundError: No module named 'ddgs'`** - newer versions of `agno` use the `ddgs` package (not the older `duckduckgo-search`) for web search. Run `pip install ddgs` or reinstall with the updated `requirements.txt`.
- **`model_not_found` / "The model `qwen/qwen3-32b` does not exist"** - Groq deprecated `qwen/qwen3-32b`. This project now uses `openai/gpt-oss-120b`, Groq's recommended free replacement. If you see this error, make sure you're using the latest version of the files in this project.
- **`GROQ_API_KEY not set`** - make sure `.env` exists in the project root (same folder as `app.py`), contains a real key (not the placeholder), and that you restarted `streamlit run app.py` after creating/editing it.
