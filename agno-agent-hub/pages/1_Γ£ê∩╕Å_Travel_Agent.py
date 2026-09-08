import streamlit as st
from dotenv import load_dotenv

from agents.travel_agent import build_travel_agent

load_dotenv()

st.set_page_config(page_title="Travel Safety Agent", page_icon="✈️")
st.title("✈️ Travel Safety Agent")
st.caption("Ask about current safety, weather, or visa info before you travel anywhere.")


@st.cache_resource
def get_agent():
    return build_travel_agent()


agent = get_agent()

if "travel_messages" not in st.session_state:
    st.session_state.travel_messages = []

for msg in st.session_state.travel_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

query = st.chat_input("e.g. Is it safe to travel to UAE today?")

if query:
    st.session_state.travel_messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Searching and analyzing..."):
            response = agent.run(query)
        st.markdown(response.content)

    st.session_state.travel_messages.append({"role": "assistant", "content": response.content})
