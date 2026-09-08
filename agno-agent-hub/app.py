import streamlit as st

st.set_page_config(
    page_title="AI Agent Hub",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 AI Agent Hub")
st.caption("Five Agno-powered AI agents in one place — pick one from the sidebar.")

st.markdown(
    """
This app bundles the following agents, all built with the **Agno framework**:

| Agent | What it does | Model | Tools |
|---|---|---|---|
| ✈️ Travel Safety Agent | Live web search for travel/safety advice | Groq `qwen3-32b` | DuckDuckGo |
| 📈 Investment Analyst | Stock price, fundamentals, recommendations | Groq `qwen3-32b` | YFinance + DuckDuckGo |
| 🧠 Memory Chat Agent | Remembers facts about the user | Groq `qwen3-32b` | SQLite memory |
| 🌐 Translator Team | Answers in English, Chinese, and Hindi at once | Groq `qwen3-32b` | Multi-agent Team |
| 🎥 YouTube Analyzer | Timestamped breakdown of a video | Groq `qwen3-32b` | YouTubeTools |

**To get started:**
1. Create a `.env` file (see `.env.example`) and add your free `GROQ_API_KEY`.
2. `pip install -r requirements.txt`
3. `streamlit run app.py`
4. Pick any agent from the sidebar and start chatting.
"""
)

st.info("👈 Select an agent from the sidebar to get started.")
