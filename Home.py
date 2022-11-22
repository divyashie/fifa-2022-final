import streamlit as st 
from PIL import Image 
import base64
from google.oauth2 import service_account
from gsheetsdb import connect
from gspread_pandas import Spread,Client
import pandas as pd 
from pandas import DataFrame

st.set_page_config(
	page_title="Coup du Monde APSIM", 
	page_icon="images/world-cup.png"
)


st.markdown("<h1 style='text-align: center; color: navy blue;'>Prédiction Apsim de la coupe du monde 2022</h1>", unsafe_allow_html=True)
st.write("Veuillez ajouter votre pronostic pour le match!")
st.markdown("<h4>Match pour le 23/11/22</h4>", unsafe_allow_html=True)

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
    c1, c2 = st.columns(2)
    with c1: 
        with st.form(country1): 
            image = Image.open(f"images/{country1}.png" ) 
            new_image = image.resize((600,400))
            st.image(new_image, caption=country1)
            text_input1 = st.text_input(
            "Entrez le score prédit 👇"
            )
            submitted1 = st.form_submit_button('Score ⚽ ')

    with c2: 
        with st.form(country2): 
            image = Image.open(f"images/{country2}.png" )
            new_image = image.resize((600,400))
            st.image(image, caption=country2)
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

def arrayCountries(name): 
    matches = {'Germany' : 'Japan', 'Spain' : 'Costa Rica', 'Morocco' : 'Croatia', 'Belgium': 'Canada'}
    res = []
    for match1, match2 in matches.items(): 
        score1, score2 = match(match1,match2)
        result = {'name': name, 'match1':match1, 'score1': score1, 'match2': match2, 'score2': score2}
        print(result)
        res.append(result)
    return res 

def submit(name): 
    res = arrayCountries(name)
    submitButton = st.button("Envoyer 💸")
    sheet = "sheet1" 
    if submitButton: 
        current_df = pd.DataFrame(res)
        current_df.head()
        df = loadSpreadsheet(sheet)
        new_df = df.append(current_df, ignore_index=True)
        updateSpreadsheet(sheet, new_df)
        st.markdown("<h4>Merci pour votre réponse</h4>",unsafe_allow_html=True)

        
def main(): 
    add_bg_from_local("images/wallpaper.png")
    name = st.text_area('Entrez votre nom', on_change=write_name, key='text_key')
    submit(name)

if __name__ == "__main__": 
    main()
