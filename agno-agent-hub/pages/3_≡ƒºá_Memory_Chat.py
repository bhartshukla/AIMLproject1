import streamlit as st
from dotenv import load_dotenv

from agents.memory_agent import build_memory_agent, get_memories

load_dotenv()

st.set_page_config(page_title="Memory Chat Agent", page_icon="🧠")
st.title("🧠 Memory Chat Agent")
st.caption("This agent remembers facts about you across conversations (stored in SQLite).")


@st.cache_resource
def get_agent():
    return build_memory_agent()


agent = get_agent()

user_id = st.text_input("Your user ID (email or any unique name)", value="guest@example.com")

if "memory_messages" not in st.session_state:
    st.session_state.memory_messages = []

for msg in st.session_state.memory_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

query = st.chat_input("e.g. I am Rahul & I am a Data Analyst.")

if query:
    st.session_state.memory_messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = agent.run(query, user_id=user_id)
        st.markdown(response.content)

    st.session_state.memory_messages.append({"role": "assistant", "content": response.content})

with st.sidebar:
    st.subheader("Stored memories")
    if st.button("Refresh memories"):
        memories = get_memories(agent, user_id)
        if memories:
            for m in memories:
                st.write(f"- {m.memory}")
        else:
            st.write("No memories stored yet.")
