import streamlit as st 
from PIL import Image 
from pathlib import Path
import base64
from google.oauth2 import service_account
from gsheetsdb import connect
from gspread_pandas import Spread,Client
import pandas as pd 
from pandas import DataFrame
import streamlit.components.v1 as components

st.set_page_config(
	page_title="Coup du Monde APSIM", 
	page_icon="images/world-cup.png", 
    initial_sidebar_state="expanded",
	layout="wide"
)

st.image("images/apsim.png", width=75)

countdown_file = open("countdown.html", 'r')
raw_file = countdown_file.read().encode("utf-8")
raw_file = base64.b64encode(raw_file).decode()
source_code = countdown_file.read()
components.iframe(f"data:text/html;base64,{raw_file}", height=400)

scope=[
         "https://www.googleapis.com/auth/spreadsheets", 'https://www.googleapis.com/auth/drive'
]
credentials = service_account.Credentials.from_service_account_info(
                st.secrets["gcp_service_account"], scopes = scope)
client = Client(scope=scope,creds=credentials)
spreadsheetname = "Database"
spread = Spread(spreadsheetname,client = client)
#st.write(spread.url)

sh = client.open(spreadsheetname)

st.markdown("<h3 style='text-align: center; color: Black;'>Third & Finals </h3>", unsafe_allow_html=True)
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover;
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

def write_name(): 
    st.write(st.session_state.text_key)

def match(country1, country2): 
    c1, mid, c2 = st.columns([1,0.25,1])
    with c1: 
        image = Image.open(f"images/{country1}.png" ) 
        new_image = image.resize((600,400))
        st.image(new_image, caption=country1)
        text_input1 = c1.text_input(
            "Entrez le score prédit 👇", key=f"{country1}"
        )
    with mid: 
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.image("images/vs.png")
    with c2: 
        image = Image.open(f"images/{country2}.png" )
        new_image = image.resize((600,400))
        st.image(image, caption=country2)
        text_input2 = c2.text_input(
            "Entrez le score prédit 👇", key=f"{country2}"
        )

    if ('score1' not in st.session_state) and (text_input1 !=''): 
        st.session_state['score1'] = text_input1
    if ('score2' not in st.session_state) and (text_input2 !=''): 
        st.session_state['score2'] = text_input2

    return text_input1, text_input2

def loadSpreadsheet(sheet): 
    worksheet= sh.worksheet(sheet)
    df = pd.DataFrame(worksheet.get_all_records())
    return df 

def updateSpreadsheet(sheet, dataframe, col): 
    spread.df_to_sheet(dataframe[col], sheet=sheet, index=False)

def arrayCountries(): 
    matches = { 'Croatia' : 'Morocco', 'Argentina' : 'France'} #change
    res = []
    col = ['name', 'match1', 'score1', 'match2', 'score2']
    with st.form('Test'): 
        name = st.text_area("Entrez le nom de l'équipe", key='text_key')
        for match1, match2 in matches.items(): 
            score1, score2 = match(match1,match2)
            result = {'name': name, 'match1':match1, 'score1': score1, 'match2': match2, 'score2': score2}
            res.append(result)
        submitButton = st.form_submit_button("Envoyer ⚽")
        if submitButton: 
            sheet = "sheet1" 
            current_df = pd.DataFrame(res)
            print(current_df)
            df = loadSpreadsheet(sheet)
            new_df = df.append(current_df, ignore_index=True)
            updateSpreadsheet(sheet, new_df, col)
            st.markdown("<h4>Merci pour votre réponse</h4>",unsafe_allow_html=True)
            
def main(): 
    add_bg_from_local("images/wallpaper-opa.png")
    arrayCountries()

if __name__ == "__main__": 
    main()
