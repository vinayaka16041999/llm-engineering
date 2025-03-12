from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import streamlit as st
from dotenv import load_dotenv
import os 
from langchain.llms import OpenAI
load_dotenv()

def generate_pet_names(pet_type, pet_color):
    
    prompt_template = PromptTemplate(input_variables=['pet_type', 'pet_color'], template=" I have a {pet_type} pet of color {pet_color} and I want a cool name for it. Suggest me 5 names for my pet")
    llm = OpenAI(temperature=0.8)
    chain = LLMChain(llm=llm, prompt=prompt_template)
    response = chain({'pet_type': pet_type, 'pet_color': pet_color})
    return response

st.title("Pet Name Generator")

st.sidebar.title("Pet Options")
pet_type = st.sidebar.selectbox("Select Pet Type", ["Dog", "Cat", "Parrot"])

if pet_type == "Dog":
    pet_color = st.sidebar.text_area("Enter Dog Color", max_chars=15)
elif pet_type == "Cat":
    pet_color = st.sidebar.text_area("Enter Cat Color", max_chars=15)
else:
    pet_color = st.sidebar.text_area("Enter Parrot Color", max_chars=15)

if pet_color:
    response = generate_pet_names(pet_type, pet_color)
    st.text(response['text'])