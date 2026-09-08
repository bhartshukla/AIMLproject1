import streamlit as st
from dotenv import load_dotenv

from agents.stock_agent import build_stock_agent

load_dotenv()

st.set_page_config(page_title="Investment Analyst", page_icon="📈")
st.title("📈 Investment Analyst")
st.caption("Ask about stock prices, fundamentals, and analyst recommendations.")


@st.cache_resource
def get_agent():
    return build_stock_agent()


agent = get_agent()

if "stock_messages" not in st.session_state:
    st.session_state.stock_messages = []

for msg in st.session_state.stock_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

query = st.chat_input("e.g. Share the MSFT stock price and analyst recommendations")

if query:
    st.session_state.stock_messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Pulling market data..."):
            response = agent.run(query)
        st.markdown(response.content)

    st.session_state.stock_messages.append({"role": "assistant", "content": response.content})
