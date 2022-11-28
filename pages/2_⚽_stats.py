import streamlit as st 
import Home as h 
from googlesearch import search 
import requests 
from bs4 import BeautifulSoup

def liveScores(matchSearch): 
    """
    GET Live Scores from Google Search 
    """
    url = f"https://google.com/search?q={matchSearch}"
    response = requests.get(url) #download html content of web page 
    matchScores = []
    try:
        if response.status_code == 200: 
            soup = BeautifulSoup(response.content, 'html.parser')
            activities = soup.find_all("div", {"class": "BNeawe deIvCb AP7Wnd"})
            retrieval = [activity.text for activity in activities]
            print(retrieval)
            if retrieval[0] == matchSearch and retrieval[1].isdigit() and retrieval[2].isdigit(): 
                #Success!
                matches = retrieval[0].split("vs")
                matches = [m.strip() for m in matches]
                scores = [int(retrieval[1]), int(retrieval[2])] 
                matchScores = matches + scores 
                return matchScores
            else: 
                print("No score in yet!") 
    except requests.exceptions.HTTPError as e: 
                print(e)
    return None 

def predictedScores(): 
    #read data from google sheets 
    existing_df = h.loadSpreadsheet(sheet='sheet1')
    m1 = existing_df['match1'].unique()
    m2 = existing_df['match2'].unique()
    matches = m1 + " vs " + m2
    print(matches)
    hash_map = {}
    for matchSearch in matches: 
        if liveScores(matchSearch) is not None: 
            hash_map[matchSearch] = liveScores(matchSearch)
            #print(hash_map)
        else: 
            continue 
    return hash_map 
    #return st.dataframe(existing_df) 


def main(): 
    st.warning("Under Construction!")
    #predictedScores()

if __name__ == "__main__": 
    main()