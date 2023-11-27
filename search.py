import streamlit as st
from google.oauth2 import service_account
from gsheetsdb import connect
import streamlit.components.v1 as components
import pandas as pd
import gspread
from datetime import datetime
import socket
import os
import webbrowser
from serpapi import BaiduSearch
from st_click_detector import click_detector
from streamlit.components.v1 import html

#### Demo: https://search-test-jiani.streamlit.app/

#### part 0. main page setting
st.set_page_config(page_title='Optima', page_icon=':robot:')
col1, col2, col3 = st.columns([1,6,1])
with col1:
    st.write("")
with col2:
    st.image("logo-optima.png", width=500)   # lumina.png
with col3:
    st.write("")
st.markdown('\n')

#### part 1. Instruction (sidebar)
st.sidebar.title("Instructions")
counter_placeholder = st.sidebar.empty()
st.sidebar.info('''
    You will be asked to complete **one task** with the Optima platform. \n 
    Please ensure that you **do not close the Qualtrics and the Optima platform pages** while completing the task. \n
    You can type in your Prolific ID and press Enter to initiate this service: \n 
    ''')
user_id = st.sidebar.text_input("Prolific ID...")   # ask for participation id


#### Connect to Google Sheets (reference: https://docs.streamlit.io/knowledge-base/tutorials/databases/private-gsheet)
# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=["https://www.googleapis.com/auth/spreadsheets",],
)
conn = connect(credentials=credentials)
client = gspread.authorize(credentials)


# Read Google Sheets
sheet_url = st.secrets["private_gsheets_url"]
sheet = client.open_by_url(sheet_url).sheet1   # select a worksheet


# Set Google Search Key (reference: https://github.com/serpapi/google-search-results-python#search-baid)
Google_API_KEY = st.secrets['Google_API_KEY']

if user_id: 
    # query = st.text_input(label=" ", placeholder="ask Lumina.AI")
    query = st.chat_input("ask Optima")
    
    if query:  # Activates the code below by hitting Enter/Return in the search textbox
        result_str = ""
        input_time = str(datetime.now())
        params = {"q": query, "device": "desktop", "hl": "en", "gl": "us", "num": "20", "api_key": Google_API_KEY, "output": "HTML"}
        
        # Define the search search
        search_result = []
        while len(search_result) < 10:
            search = BaiduSearch(params)
            json_results = search.get_json()
            search_result = json_results['organic_results']
        
        # Initializing the data frame that stores the results
        result_str = ""
        save_str = " "
        for n, i in enumerate(search_result): #iterating through the search results
            # Step1. read from retrieved results. 
            individual_search_result = i
            url_txt = individual_search_result['title'] #Finding the title of the individual search result
            url_displayed = individual_search_result['displayed_link']
            href = individual_search_result['link'] #title's URL of the individual search result
            # (exception handle) In a few cases few individual search results doesn't have a description. In such cases the description would be blank
            if individual_search_result.get('snippet') != None:
                description = individual_search_result['snippet']
            else:
                description = " "    
            if n < 10:
                result_str += f'<tr style="border: none;"></tr>'+\
                f'<tr style="border: none;"></tr>'+\
                f'<tr style="border: none;">{url_displayed}</tr>'+\
                f'<tr style="border: none;"><h4><a href="{href}" target="_blank">{url_txt}</a></h4></tr>'+\
                f'<tr style="border: none;">{description}</tr>'+\
                f'<hr></hr>'

                ### save in Google Sheets
                output_time = str(datetime.now())
                save_str += " [" + str(n) + "] " + url_displayed + "|||||" + url_txt + "|||||" + href + "|||||" + description
                #row = [user_id, input_time, query, output_time, save_str]
                #sheet.insert_row(row)
            else:  # more than 10 results
                pass

        row = [user_id, input_time, query, output_time, save_str]
        sheet.insert_row(row)
        st.markdown(f'{result_str}', unsafe_allow_html=True)

else:    
    st.markdown("\n")
    st.markdown("<h2 style='text-align: center;'>Please read instructions in the sidebar carefully and \n type in your Prolific ID to initiate this service!</h2>", unsafe_allow_html=True)
