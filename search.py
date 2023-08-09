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
from serpapi import GoogleSearch
from st_click_detector import click_detector
from streamlit.components.v1 import html

#### Demo: https://search-test-jiani.streamlit.app/

#### part 0. main page setting
st.set_page_config(page_title='Lumina.AI', page_icon=':robot:')
col1, col2, col3 = st.columns([1,6,1])
with col1:
    st.write("")
with col2:
    st.image("lumina.png", width=500)
with col3:
    st.write("")
# st.image(image='lumina.png', width=500)
st.markdown('\n')

#### part 1. Instruction (sidebar)
st.sidebar.title("Instruction")
counter_placeholder = st.sidebar.empty()
st.sidebar.info('''
    You will be asked to complete **three tasks** with Lumina. AI. \n 
    Please ensure that you **do not close the Qualtrics and Lumina. AI pages** while completing your tasks. \n
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


#### Set Google Search Key (reference: https://github.com/serpapi/google-search-results-python)
Google_API_KEY = st.secrets['Google_API_KEY']

def nav_to(url):
    js = f'window.open("{url}", "_blank").then(r => window.parent.location.href);'
    st_javascript(js)
    
if user_id: 
    # query = st.text_input(label=" ", placeholder="ask Lumina.AI")
    query = st.chat_input("ask Lumina.AI")
    
    if query: #Activates the code below on hitting Enter/Return in the search textbox
        result_str = ""
        input_time = str(datetime.now())
        params = {"q": query, "device": "desktop", "hl": "en", "gl": "us", "num": "10", "api_key": Google_API_KEY, "output": "HTML"}
        # define the search search
        search = GoogleSearch(params)
        json_results = search.get_json()
        search_result = json_results['organic_results']
        # out_html = search.get_html()
        # present
        # components.html(out_html)
    
        result_df = pd.DataFrame() # Initializing the data frame that stores the results
        result_str = ""
        save_str = ""
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
                
            # Present and Save the result data frame after processing each individual search result
            # def click_button(href, st.session_state):
            #    st.session_state[href] = True
            #    webbrowser.open_new_tab(href)
                # open_page(href)
                # st.write(st.session_state)
            #def click_button(href):
            #    st.session_state[href] = True
            #    nav_to(href)
            #    # components.iframe(href)
            #    # webbrowser.open_new_tab(href)
            #    # st.write(f"Button {href} Clicked!")
                
            #hrefs = []
            if n < 10:
                #if href not in st.session_state:
                #    st.session_state[href] = False   
                #st.markdown('\n')
                #st.write(url_displayed)
                #st.button(url_txt, on_click=click_button, args=(hrefs))
                #st.markdown(description)
                #st.divider()
                #hrefs.append(href)

                result_str += f'<tr style="border: none;"></tr>'+\
                f'<tr style="border: none;"></tr>'+\
                f'<tr style="border: none;">{url_displayed}</tr>'+\
                f'<tr style="border: none;"><h4><a href="{href}" target="_blank">{url_txt}</a></h4></tr>'+\
                f'<tr style="border: none;">{description}</tr>'+\
                f'<hr></hr>'

                ### save in Google Sheets
                output_time = str(datetime.now())
                save_str = "[" + str(n) + "] " + url_displayed + "|||||" + url_txt + "|||||" + href + "|||||" + description
                row = [user_id, input_time, query, output_time, save_str]
                sheet.insert_row(row)
            else:
                pass
                
        st.markdown(f'{result_str}', unsafe_allow_html=True)

        #if click_detector(result_str):
        #    st.write(result_str)
        #    clicked = click_detector(result_str)
        #    st.markdown(f"**{clicked} clicked**" if clicked != "" else "")
        # st.write(st.session_state)
        # for href in hrefs:
        #    if st.session_state[href]:
        #        st.write(st.session_state)
                # webbrowser.open_new_tab(href)
                # st.write(f"Button {href} Clicked!")
        
else:    
    # st.header("")
    st.markdown("\n")
    st.markdown("<h1 style='text-align: center;'>Please read instructions in the sidebar carefully and \n type in your Prolific ID to initiate this service!</h1>", unsafe_allow_html=True)
