import streamlit as st
import importlib
kb = importlib.import_module('3_knowledge_base')
import textwrap

st.title('LLM With FAISS Knowledge base')

with st.sidebar:
    with st.form(key='my-form'):
        youtube_url = st.sidebar.text_area(label = "Enter your url here", max_chars=100)
        query = st.sidebar.text_area(label = "Enter your question here", max_chars=100)
        submit_button = st.form_submit_button(label='Submit')
if query and youtube_url:
    db = kb.create_vector_db(youtube_url)
    response = kb.get_relevant_data(db, query)

    st.subheader("Answer:")
    st.write(textwrap.fill(response, 1000))


