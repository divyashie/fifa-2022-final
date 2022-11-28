import streamlit as st 
import Home as h 
from googlesearch import search 
import pandas as pd 
import requests 
from bs4 import BeautifulSoup

SHEET_ID = '1GdZDJVy1RPSiwwyQcnMg6RiWzlRIGOslbia2hfRcHys'
SHEET_NAME = 'Evaluate'
url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'

# df = pd.read_csv(url,error_bad_lines=False)
# print(df.head(100))
def main(): 
    st.warning("Under Construction!")

if __name__ == "__main__": 
    main()