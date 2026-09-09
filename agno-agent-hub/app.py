import streamlit as st

st.set_page_config(
    page_title="AI Agent Hub",
    layout="centered",
)

st.title("AI Agent Hub")
st.caption("Five Agno-powered AI agents in one place - pick one from the sidebar.")

st.markdown(
    """
This app bundles the following agents, all built with the **Agno framework**:

| Agent | What it does | Model | Tools |
|---|---|---|---|
| Travel Safety Agent | Live web search for travel/safety advice | Groq `gpt-oss-120b` | DuckDuckGo |
| Investment Analyst | Stock price, fundamentals, recommendations | Groq `gpt-oss-120b` | YFinance + DuckDuckGo |
| Memory Chat Agent | Remembers facts about the user | Groq `gpt-oss-120b` | SQLite memory |
| Translator Team | Answers in English, Chinese, and Hindi at once | Groq `gpt-oss-120b` | Multi-agent Team |
| YouTube Analyzer | Timestamped breakdown of a video | Groq `gpt-oss-120b` | YouTubeTools |

**To get started:**
1. Create a `.env` file (see `.env.example`) and add your free `GROQ_API_KEY`.
2. `pip install -r requirements.txt`
3. `streamlit run app.py`
4. Pick any agent from the sidebar and start chatting.
"""
)

st.info("Select an agent from the sidebar to get started.")
