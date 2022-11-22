import streamlit as st 
from PIL import Image 
from google.oauth2 import service_account
from gsheetsdb import connect
from gspread_pandas import Spread,Client
import pandas as pd 
from pandas import DataFrame

st.set_page_config(
	page_title="Coup du Monde APSIM", 
	page_icon="images/world-cup.png",
	initial_sidebar_state="expanded",
	layout="wide"
	)

st.markdown("<h1 style='text-align: center; color: navy blue;'>Prédiction Apsim de la coupe du monde 2022</h1>", unsafe_allow_html=True)
st.write("Veuillez ajouter votre pronostic pour le match!")

scope=[
         "https://www.googleapis.com/auth/spreadsheets", 'https://www.googleapis.com/auth/drive'
]

credentials = service_account.Credentials.from_service_account_info(
                st.secrets["gcp_service_account"], scopes = scope)
client = Client(scope=scope,creds=credentials)
spreadsheetname = "Database"
spread = Spread(spreadsheetname,client = client)
st.write(spread.url)

sh = client.open(spreadsheetname)

def write_name(): 
    st.write(st.session_state.text_key)

def show_country(): 
    c1, c2 = st.columns(2)
    with c1: 
        with st.form('Form1'): 
            image = Image.open('images/qatar.png') 
            new_image = image.resize((600,400))
            st.image(new_image, caption='Qatar')
            text_input1 = st.text_input(
            "Entrez le score prédit 👇"
            )
            submitted1 = st.form_submit_button('Score ⚽ ')


    with c2: 
        with st.form('Form2'): 
            image = Image.open('images/Ecuador.png')
            new_image = image.resize((600,400))
            st.image(image, caption='Ecuador')
            text_input2 = st.text_input(
            "Entrez le score prédit 👇"
            )
            submitted2 = st.form_submit_button('Score ⚽')   
    return text_input1, text_input2

def loadSpreadsheet(sheet): 
    worksheet= sh.worksheet(sheet)
    df = DataFrame(worksheet.get_all_records())
    return df 

def updateSpreadsheet(sheet, dataframe): 
    col = ['name', 'match1', 'score1', 'match2', 'score2']
    spread.df_to_sheet(dataframe[col], sheet=sheet, index=False)

def submit(name, score1, score2): 
    submitButton = st.button("Envoyer 💸")
    match1 = "Qatar"
    match2 = "Ecuador"
    sheet = "sheet1" 

    if submitButton: 
        my_dict = {'name': name, 'match1':match1, 'score1': score1, 'match2': match2, 'score2': score2}
        current_df = pd.DataFrame([my_dict])
        df = loadSpreadsheet(sheet)
        new_df = df.append(current_df, ignore_index=True)
        updateSpreadsheet(sheet, new_df)
        st.markdown("<h4>Merci pour votre réponse</h4>",unsafe_allow_html=True)

        
def main(): 
    name = st.text_area('Entrez votre nom', on_change=write_name, key='text_key')
    score1, score2 = show_country()
    submit(name,score1,score2)

if __name__ == "__main__": 
    main()
