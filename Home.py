import streamlit as st 
from PIL import Image 
import sqlite3
from sqlite3 import Connection

URI_SQLITE_DB = "test.db"

# # Store the initial value of widgets in session state
# if "visibility" not in st.session_state:
#     st.session_state.visibility = "visible"
#     st.session_state.disabled = False

st.set_page_config(
	page_title="Coup du Monde APSIM", 
	page_icon="images/world-cup.png",
	initial_sidebar_state="expanded",
	layout="wide"
	)

st.markdown("<h1 style='text-align: center; color: navy blue;'>Prédiction Apsim de la coupe du monde 2022</h1>", unsafe_allow_html=True)
st.write("Veuillez ajouter votre pronostic pour le match!")

    
def init_db(conn: Connection):
    conn.execute(
        """CREATE TABLE IF NOT EXISTS test
            (
                NAME TEXT,
                SCORE1 INT, 
                SCORE2 INT 
            );"""
    )
    conn.commit()

@st.cache(hash_funcs={Connection: id})
def get_connection(path:str):
    return sqlite3.connect(path, check_same_thread=False)

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
            # label_visibility=st.session_state.visibility,
            # disabled=st.session_state.disabled, 
            # key="placeholder"
            )
            submitted1 = st.form_submit_button('Score ⚽ ')


    with c2: 
        with st.form('Form2'): 
            image = Image.open('images/Ecuador.png')
            new_image = image.resize((600,400))
            st.image(image, caption='Ecuador')
            text_input2 = st.text_input(
            "Entrez le score prédit 👇"
            # label_visibility=st.session_state.visibility,
            # disabled=st.session_state.disabled, 
            # placeholder=st.session_state.placeholder, 
            )
            submitted2 = st.form_submit_button('Score ⚽')   
    return text_input1, text_input2

def submit(conn: Connection, name, score1, score2): 
    with st.form("key1"): 
        button_check = st.form_submit_button("Envoyer 💸")
        if button_check: 
            conn.execute(f"INSERT INTO test (NAME, SCORE1, SCORE2) VALUES {name, score1, score2}")
            conn.commit()

def main(): 
    name = st.text_area('Entrez votre nom', on_change=write_name, key='text_key')
    score1, score2 = show_country()
    conn = get_connection(URI_SQLITE_DB)
    init_db(conn)
    submit(conn,name,score1,score2)

if __name__ == "__main__": 
    main()