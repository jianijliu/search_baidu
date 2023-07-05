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


#### Test HTML
components.html("""
<html>
    <head>
        <title>Google Clone</title>
        <link rel="stylesheet" href="style.css">
    </head>
    <body>
        <header id="header">
            <ul>
                <li><a class="header-list" href="#">Gmail</a></li>
                <li><a class="header-list" href="#">Images</a></li>
                <li><a class="header-list" href="#">Account</a></li>
            </ul>
        </header>
        <div id="logo"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Google_2015_logo.svg/1200px-Google_2015_logo.svg.png" alt="Connect to Internet to view Google Logo"></div>
        <div id="search-box">
            <form action="post">
                <input placeholder="  Enter to Search here.." type="search">
                <br>
                <button class="button" type="button">Google Search</button>
                <button class="button" type="button">I'm Feeling Lucky</button>
            </form>
            <br>
            <p>Google offered in: <a href="#">हिन्दी</a><a href="#">  বাংলা</a><a href="#">  తెలుగు</a><a href="#">  मराठी</a><a href="#">
                  தமிழ்</a><a href="#">  ગુજરાતી</a><a href="#">  ಕನ್ನಡ</a><a href="#">  മലയാളം</a><a href="#">  ਪੰਜਾਬੀ</a> </p>
        </div>
        <div class="bottom">
            <div class="bottombars">
                <ul>
                    <li><a href="#" class="bottomlinks" style="font-size: 16px;">India</a></li>
                </ul>
            </div>
            <div class="bottombars">
                <ul>
                    <li style="font-size: 15px;" class="bot-left"><a href="#"  class="bottomlinks">Advertising</a></li>
                    <li style="font-size: 15px;" class="bot-left"><a href="#"  class="bottomlinks">Business</a></li>
                    <li style="font-size: 15px;" class="bot-left"><a href="#"  class="bottomlinks">About</a></li>
                    <li style="font-size: 15px;" class="bot-right"><a href="#"  class="bottomrightlinks">Settings</a></li>
                    <li style="font-size: 15px;" class="bot-right"><a href="#"  class="bottomrightlinks">Terms</a></li>
                    <li style="font-size: 15px;" class="bot-right"><a href="#" class="bottomrightlinks">Privacy</a></li>
                </ul>
            </div>
        </div>            
    </body>
</html>

""")


#### Test. Present HTML (reference: https://github.com/serpapi/google-search-results-python)
Google_API_KEY = st.secrets['Google_API_KEY']


query = st.text_input("Search")   # ask for participation id
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
