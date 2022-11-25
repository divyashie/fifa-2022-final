# Read from one spreadsheet --> write results on another spreadsheet 
# Create the Evaluate collect in the spreadsheet 
# Get the values from googlesearch api 
# Aggregate results per team 
# Display results as a graph with plotly 

# import streamlit as st 
# import Home as h 
# from googlesearch import search 
# import requests 
# from bs4 import BeautifulSoup

#read data from google sheets 
# existing_df = h.loadSpreadsheet(sheet='sheet1')

# 2 lists of same length 
# m1 = existing_df['match1'].unique()
# m2 = existing_df['match2'].unique()

# hash = {}
# def actualScores(): 
#     for i in len(m1): 
#         #formulate google search here 
#         if m1[i] 

# text = "Argentina vs Saudi Arabia"
# url = "https://google.com/search?q=" + text
# print(url)

# response = requests.get(url) #downloading html content of web page 
# if response.status_code == 200: 
#     soup = BeautifulSoup(response.content, 'html.parser')
#     #divs = soup.find_all("div", class_="imso_mh__ma-sc-cont") 
#     divs = soup.find_all("div", { "class" : "imso_mh__ma-sc-cont"}) 
#     for each_div in divs: 
#         print(each_div)

# class you get the score is: 
# <div class="imso_mh__l-tm-sc imso_mh__scr-it imso-light-font">1</div>


import streamlit as st 

st.warning("Under Construction!")