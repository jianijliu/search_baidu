import streamlit as st
from google.oauth2 import service_account
from gsheetsdb import connect
import streamlit.components.v1 as components
import pandas as pd
import gspread
from datetime import datetime
import socket
from serpapi import GoogleSearch
from st_click_detector import click_detector

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
    You will be asked to use the recommendation AI, Lumina, to **generate a recipe**. \n
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

# st.markdown('<h1 style="background-color: gainsboro; padding-left: 10px; padding-bottom: 20px;">Google Search</h1>', unsafe_allow_html=True)


if user_id: 
    # query = st.text_input(label=" ", placeholder="ask Lumina.AI")
    query = st.chat_input("ask Lumina.AI")
    
    if query: #Activates the code below on hitting Enter/Return in the search textbox
        result_str = ""
        input_time = str(datetime.now())
        params = {"q": query, "device": "desktop", "hl": "en", "gl": "us", "num": "20", "api_key": Google_API_KEY, "output": "HTML"}
        # define the search search
        search = GoogleSearch(params)
        json_results = search.get_json()
        search_result = json_results['organic_results']
        # out_html = search.get_html()
        # present
        # components.html(out_html)
    
        result_df = pd.DataFrame() #Initializing the data frame that stores the results
        result_str = ""
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
                
            # Present and Save the result data frame after processing each individual search result
            ########################################################
            ######### HTML code to display search results ##########
            ########################################################
            if n < 10:
                st.button(href)
                result_str += f'<tr style="border: none;"><h5><a href="{href}" id="Link {str(n)}" target="_blank">https://www.google.com</a></h5></tr>'
                #result_str += f'<tr style="border: none;"></tr>'+\
                #f'<tr style="border: none;"></tr>'+\
                #f'<tr style="border: none;">{url_displayed}</tr>'+\
                #f'<tr style="border: none;"><h5><a href="{href}" id="Link {str(n)}" target="_blank">{url_txt}</a></h5></tr>'+\
                #f'<tr style="border: none;">{description}</tr>'+\
                #f'<tr></tr>'+\
                #f'<tr></tr>'+\
                #f'<tr style="border: none;"><td style="border: none;"></td></tr>'
                output_time = str(datetime.now())
                save_str = "[" + str(n) + "] " + url_displayed + "|||||" + href + "|||||" + description
                row = [user_id, input_time, query, output_time, save_str]
                sheet.insert_row(row)
            else:
                pass
        
        # result_str += '</table></html>'            
        # st.markdown(f'{result_str}', unsafe_allow_html=True)

        # record clicks
        #if result_str:
        clicked = click_detector(result_str)                
        st.markdown(f"**{clicked} clicked**" if clicked != "" else "")
        clicked = click_detector(result_str, value = "new")   

        # st.markdown(clicked)
        # sheet.insert_row(clicked)
        
else:    
    # st.header("")
    st.markdown("\n")
    st.markdown("<h5 style='text-align: center;'>Please read instructions in the sidebar carefully and \n type in your participant ID first!</h5>", unsafe_allow_html=True)
