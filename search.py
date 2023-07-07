import streamlit as st
from google.oauth2 import service_account
from gsheetsdb import connect
import streamlit.components.v1 as components
import pandas as pd
import gspread
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


if user_id: 
    st.markdown('<h1 style="background-color: gainsboro; padding-left: 10px; padding-bottom: 20px;">Google Search</h1>', unsafe_allow_html=True)
    st.markdown('\n')

    col1, col2 = st.columns([1.5, 3])
    with col1:
        st.image(image='GoogleSearch.png', width=150)
    with col2:
        query = st.text_input(label=" ", placeholder="Search")
        
    if query: #Activates the code below on hitting Enter/Return in the search textbox
        input_time = str(datetime.now())
        params = {"q": query, "device": "desktop", "hl": "en", "gl": "us", "num": "13", "api_key": Google_API_KEY, "output": "HTML"}
        # define the search search
        search = GoogleSearch(params)
        json_results = search.get_json()
        search_result = json_results['organic_results']
        # out_html = search.get_html()
        # present
        # components.html(out_html)
    
        result_df = pd.DataFrame() #Initializing the data frame that stores the results
        result_str = "<html>"
        save_str = ""
        for n, i in enumerate(search_result): #iterating through the search results
            individual_search_result = i
            url_txt = individual_search_result['title'] #Finding the title of the individual search result
            url_displayed = individual_search_result['displayed_link']
            href = individual_search_result['link'] #title's URL of the individual search result
            # In a few cases few individual search results doesn't have a description. In such cases the description would be blank
            if individual_search_result.get('snippet') != None:
                description = individual_search_result['snippet']
            else:
                description = " "            
            # Present the result data frame after processing each individual search result
            ########################################################
            ######### HTML code to display search results ##########
            ########################################################
            #st.markdown(f'<tr style="border: none;"></tr>', unsafe_allow_html=True)
            #st.markdown(f'<tr style="border: none;">{url_displayed}</tr>', unsafe_allow_html=True)
            #st.markdown(f'<tr style="border: none;"><h4><a href="{href}" target="_blank">{url_txt}</a></h4></tr>', unsafe_allow_html=True)

            result_str += f'<tr style="border: none;"></tr>'+\
            f'<tr style="border: none;"></tr>'+\
            f'<tr style="border: none;">{url_displayed}</tr>'+\
            f'<tr style="border: none;"><h4><a href="{href}" target="_blank">{url_txt}</a></h4></tr>'+\
            f'<tr style="border: none;">{description}</tr>'+\
            f'<tr></tr>'+\
            f'<tr></tr>'+\
            f'<tr style="border: none;"><td style="border: none;"></td></tr>'
            save_str = "[" + n + "] " + url_displayed + "_____" + href + "_____" + description + "///"
            row = [user_id, input_time, query, output_time, save_str]
            sheet.insert_row(row)
        
        # result_str += '</table></html>'            
        st.markdown(f'{result_str}', unsafe_allow_html=True)
        output_time = str(datetime.now())
        

else:
    st.markdown("\n")
    st.markdown("Please read instructions in the sidebar carefully and type in your participant ID first!")
