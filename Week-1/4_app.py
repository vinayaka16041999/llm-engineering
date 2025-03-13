import streamlit as st
import importlib
ai = importlib.import_module('4_chatbot_w_memory')
import textwrap

st.title('LLM With Memory')

def clear_chat():
    st.session_state.messages = []
    ai.clear_memory()

with st.sidebar: 
    model = st.selectbox("Select Model", ["gpt-4o-mini", "gpt-4o", "o3-mini-2025-01-31"], key="model_name")               
    st.button("Clear Memory", on_click=ai.clear_memory)
    st.button("Clear Chat", on_click=clear_chat)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = ai.chat(model,prompt)
    with st.chat_message("bot"):
        st.markdown(response)
    st.session_state.messages.append({"role": "bot", "content": response})

