import streamlit as st
import Home as h  
import numpy as np
from pathlib import Path 

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
     # CSS to inject contained in a string
    hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                """

    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)

    df['name'] = df['name'].str.strip()
    scores = df.groupby(['name'], as_index=False).sum()
    scores.columns = ["nom d'équipe", "résultat"]
    scores = scores.sort_values(by="résultat", ascending=False)
    st.table(scores) 

def winnerAnnouncement(): 
    st.markdown("<h4>Equipe en tête: <b>Thierry</b></h4>", unsafe_allow_html=True)
    img_path = "images/winner_logo.png"
    # img_bytes = Path(img_path).read_bytes()
    # encoded = h.base64.b64encode(img_bytes).decode()
    # img_html = "<img src='data:image/png;base64,{}' class='img-fluid'>".format(
    #   encoded 
    # )
    # st.markdown(img_html, unsafe_allow_html=True)
    # st.markdown("Equipe de <b>Thierry</b> en tête.", unsafe_allow_html=True)
    col1, mid, col2 = st.columns([1,1,1])
    with col1: 
        st.image(img_path)
    st.balloons()

def main(): 
    df = scoreLogic()
    aggregateScores(df)
    winnerAnnouncement()

if __name__ == "__main__": 
    main()