import streamlit as st
from dotenv import load_dotenv

from agents.youtube_agent import build_youtube_agent

load_dotenv()

st.set_page_config(page_title="YouTube Video Analyzer", page_icon="🎥")
st.title("🎥 AI YouTube Video Analyzer")
st.caption("Paste a video link and get a timestamped breakdown.")


@st.cache_resource
def get_agent():
    return build_youtube_agent()


agent = get_agent()

video_url = st.text_input("Enter YouTube Video Link")
button = st.button("Analyze Video")

if video_url and button:
    with st.spinner("Analyzing video..."):
        response = agent.run(f"Analyze this video: {video_url}")

    st.markdown("### Analysis Report of Video")
    st.markdown(response.content)
