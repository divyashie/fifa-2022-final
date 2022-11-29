import streamlit as st
import Home as h  
import pandas as pd 
import numpy as np

st.subheader("Bienvenue à la page des scores!")
st.markdown("Voici les détails de la compilation des scores: ")
st.markdown("<ul><li>Prédiction exacte du score = <b>3 points</b></ul></li>",unsafe_allow_html=True)
st.markdown("<ul><li>Prédiction de l'équipe gagnante ou du match nul = <b>1 point</b></ul></li>",unsafe_allow_html=True)
st.markdown("<ul><li>le défault = <b>0 point</b></ul></li>",unsafe_allow_html=True)

def scoreLogic(): 
    df = h.loadSpreadsheet('evaluate') 
    df.columns = df.iloc[0]  #set first row of dataframe to column names 
    df = df[1:] #set the data starting from second row 
    conditions = [((df['score1'] == df['actual1']) & (df['score2'] == df['actual2'])), 
                  (((df['score1'] > df['score2']) & (df['actual1'] > df['actual2'])) | ((df['score2'] > df['score1']) & (df['actual2'] > df['actual1']))), 
                  (((df['score1'] == df['score2']) & (df['actual1'] == df['actual2'])))
                  ]
    choices = [3, 1, 1]
    df['result'] = np.select(conditions, choices, default=0)
    return df
    
def aggregateScores(df): 
    df['name'] = df['name'].str.strip()
    st.dataframe(df.groupby(['name']).sum()) 

def main(): 
    df = scoreLogic()
    aggregateScores(df)

if __name__ == "__main__": 
    main()