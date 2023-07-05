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

st.markdown('<h1 style="background-color: gainsboro; padding-left: 10px; padding-bottom: 20px;">Google Search</h1>', unsafe_allow_html=True)
st.markdown('\n')

col1, col2, col3 = st.columns(3)
with col1:
    st.image(image='GoogleSearch.png', width=150)
with col2 and col3:
    query = st.text_input(label=" ", placeholder="Search")

if query: #Activates the code below on hitting Enter/Return in the search textbox
    params = {"q": query, "device": "desktop", "hl": "en", "gl": "us", "num": "10", "api_key": Google_API_KEY, "output": "HTML"}
    # define the search search
    search = GoogleSearch(params)
    json_results = search.get_json()
    search_result = json_results['organic_results']
    # out_html = search.get_html()
    # present
    # components.html(out_html)
    
    result_df = pd.DataFrame() #Initializing the data frame that stores the results
    result_str = ""
    for n, i in enumerate(search_result): #iterating through the search results
        individual_search_result = i
        #individual_search_result = BeautifulSoup(i, features="html.parser") #converting individual search result into a BeautifulSoup object
        url_txt = individual_search_result['title'] #Finding the title of the individual search result
        href = individual_search_result['link'] #title's URL of the individual search result
        # In a few cases few individual search results doesn't have a description. In such cases the description would be blank
        description = "" if individual_search_result['snippet'] is None else individual_search_result['snippet']
        # Appending the result data frame after processing each individual search result
        #result_df = result_df.append(pd.DataFrame({"Title": url_txt, "URL": href, "Description": description}, index=[n]))
        #count_str = f'<b style="font-size:20px;">Google Search returned {len(result_df)} results</b>'
        ########################################################
        ######### HTML code to display search results ##########
        ########################################################
        result_str += f'<tr style="border: none;"><h3><a href="{href}" target="_blank">{url_txt}</a></h3></tr>'+\
        f'<tr style="border: none;">{description}</tr>'+\
        f'<tr style="border: none;"><td style="border: none;"></td></tr>'
    result_str += '</table></html>'
                
    #st.markdown(f'{count_str}', unsafe_allow_html=True)
    st.markdown(f'{result_str}', unsafe_allow_html=True)
    #st.markdown('<h3>Data Frame of the above search result</h3>', unsafe_allow_html=True)
    #st.dataframe(result_df)

# else:
#    st.markdown("\n")
#    st.markdown("Please read instructions in the sidebar carefully and type in your participant ID first!")
