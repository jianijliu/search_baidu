import streamlit as st
from google.oauth2 import service_account
from gsheetsdb import connect
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime
import socket
from serpapi import GoogleSearch


#### part 0. main page setting
#st.set_page_config(page_title='ggsearch-Jiani', page_icon=':robot:')
#st.header("Ask Google")


#### part 1. Instruction (sidebar)
st.sidebar.title("Instruction")
counter_placeholder = st.sidebar.empty()
st.sidebar.info('''
    You will be asked to have a conversation with ChatGPT to **generate a recipe**. \n
    Following the chat, you’ll be redirected back to the survey to answer a few final questions and receive your payment code. 
    \n Please paste down your participation ID and press Enter to submit: 
    ''')
user_id = st.sidebar.text_input("Participation ID...")   # ask for participation id


#### Test. Present HTML (reference: https://github.com/serpapi/google-search-results-python)
Google_API_KEY = st.secrets['Google_API_KEY']

st.image(image='GoogleSearch.png', width=600)
query = st.text_input(label="", placeholder="Search")   # ask for participation id

if query:
    params = {
        "q": query, "device": "desktop", "hl": "en", "gl": "us", "num": "10", "api_key": Google_API_KEY,"output": "HTML"}
    # define the search search
    search = GoogleSearch(params)
    out_html = search.get_html()
    # present
    #components.html(out_html)


#else:
#    st.markdown("\n")
#    st.markdown("Please read instructions in the sidebar carefully and type in your participant ID first!")
