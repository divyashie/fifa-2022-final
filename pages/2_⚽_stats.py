import streamlit as st
import Home as h  
import numpy as np
import pandas as pd 
import plotly.express as px
from pathlib import Path 
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import JsCode
from streamlit.components.v1 import html 

st.markdown("<h1 style='text-align: center; color: navy blue;'>Bienvenue à la page des scores</h1>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1: 
    st.image("images/Qatar_wallpaper.png",width=600)
with col2: 
    st.write(" ")
    st.write(" ")
    st.markdown("Voici les détails de la compilation des scores: ")
    st.markdown("<ul><li> Prédiction exacte du score = <b>3 points 🏆 </b></ul></li>",unsafe_allow_html=True)
    st.markdown("<ul><li>Prédiction de l'équipe gagnante ou du match nul = <b>1 point 🏅 </b></ul></li>",unsafe_allow_html=True)
    st.markdown("<ul><li>le défault = <b>0 point 🍀 </b></ul></li>",unsafe_allow_html=True)

def scoreLogic(): 
    worksheet = h.sh.worksheet('evaluate')
    df = pd.DataFrame(worksheet.get_all_values())
    #df = h.loadSpreadsheet('evaluate') 
    df.columns = df.iloc[0]  #set first row of dataframe to column names 
    df = df[1:] #set the data starting from second row 
    conditions = [((df['score1'] == df['actual1']) & (df['score2'] == df['actual2'])), 
                  (((df['score1'] > df['score2']) & (df['actual1'] > df['actual2'])) | ((df['score2'] > df['score1']) & (df['actual2'] > df['actual1']))), 
                  (((df['score1'] == df['score2']) & (df['actual1'] == df['actual2'])))
                  ]
    choices = [3, 1, 1]
    df['result'] = np.select(conditions, choices, default=0)
    return df

def flagEmoji(df): 
    flags = {"Argentina" : "🇦🇷", "Australia" : "🇦🇺", "Belgium" : "🇧🇪", "Brazil" : "🇧🇷", "Cameroon" : "🇨🇲", "Canada" : "🇨🇦", "Costa Rica" : "🇨🇷", 
        "Croatia" : "🇭🇷", "Denmark" : "🇩🇰", "Ecuador" : "🇪🇨", "England" : "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "France" : "🇫🇷", "Germany" : "🇩🇪", "Ghana" : "🇬🇭", "Iran" : "🇮🇷", 
        "Japan" : "🇯🇵", "Mexico" : "🇲🇽", "Morocco": "🇲🇦", "Netherlands" : "🇳🇱", "Poland" : "🇵🇱", "Portugal": "🇵🇹", "Qatar" : "🇶🇦", "Saudi Arabia" : "🇸🇦", 
        "Senegal" : "🇸🇳", "South Korea" : "🇰🇷", "Spain" : "🇪🇸", "Switzerland" : "🇨🇭", "Serbia" : "🇷🇸", "Tunisia" : "🇹🇳", "Uruguay" : "🇺🇾", "USA" : "🇺🇸", "Wales" : "🏴󠁧󠁢󠁷󠁬󠁳󠁿"
    }
    df['match1'] = df['match1'].map(flags) + " " +  df['match1']
    df['match2'] = df['match2'].map(flags) + " " + df['match2']
    return df 

def displayTeam(df): 
    df['name'] = df['name'].str.strip()
    with st.expander("Voir les Scores par équipe"): 
        option = st.selectbox("Choisir l'équipe", df['name'].unique())
        #select 
        if option: 
            st.subheader(f"Tu as choisi l'équipe de {option}")
            show_scores = df.loc[df['name'] == option]
            show_scores = show_scores[["match1", "match2", "score1", "score2", "actual1", "actual2", "result"]]

        gb = GridOptionsBuilder.from_dataframe(show_scores.tail(5))
        gb.configure_pagination()
        gb.configure_side_bar()
        gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)

        cellstyle_jscode = JsCode(
            """
            function(params) {
                if (params.value == '3'){
                    return {
                        'color' : 'black', 
                        'backgroundColor' : 'green',  
                    }
                } if (params.value == '1') {
                    return {
                        'color' : 'white', 
                        'background-color': 'orange', 
                    }
                } else {
                    return {
                        'color' : 'white', 
                        'backgroundColor' : 'red', 
                    }
                }
            }; 
            """
        )
        gb.configure_column("result", cellStyle=cellstyle_jscode)
        gridOptions = gb.build()

        AgGrid(show_scores, gridOptions=gridOptions, theme='material', enable_enterprise_modules=True,allow_unsafe_jscode=True)
       

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
    
    #draw table scores 
    fig = px.bar(scores, x="nom d'équipe", y="résultat", color="nom d'équipe")
    st.plotly_chart(fig, use_container_width=True)

    return scores 

def winnerAnnouncement(winner): 
    st.markdown(f"<h4>Equipe en tête: <b>{winner}</b> <img src='images/winner_logo.png' alt=""></h4>", unsafe_allow_html=True)
    st.image(f"images/{winner}.png", use_column_width="wide")
    st.balloons()

def main(): 
    print()
    df = scoreLogic()
    df = flagEmoji(df)
    displayTeam(df)
    scores = aggregateScores(df)
    winner = scores["nom d'équipe"].iloc[0]
    winnerAnnouncement(winner)

if __name__ == "__main__": 
    main()