import streamlit as st
from google.oauth2 import service_account
from gsheetsdb import connect
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime
import socket
from serpapi import GoogleSearch

#### Test. Present HTML (reference: https://github.com/serpapi/google-search-results-python)
Google_API_KEY = st.secrets['Google_API_KEY']

query =
params = {
    "q": query,
    "device": "desktop",
    "hl": "en",
    "gl": "us",
    "num": "10",
    "api_key": Google_API_KEY,
    "output": "html"
}
# define the search search
search = GoogleSearch(params)
out_html = search.get_html()
# present
components.html(out_html)