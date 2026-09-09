import streamlit as st
from dotenv import load_dotenv

from agents.translator_team import build_translator_team

load_dotenv()

st.set_page_config(page_title="Translator Team")
st.title("Answer & Translation Team")
st.caption("One question, answered in English, Chinese, and Hindi all at once.")


@st.cache_resource
def get_team():
    return build_translator_team()


team = get_team()

query = st.text_input("Type your question", value="What is the capital of India?")
button = st.button("Get answers in all languages")

if button and query:
    with st.spinner("Consulting all three agents..."):
        response = team.run(query)
    st.markdown(response.content)
