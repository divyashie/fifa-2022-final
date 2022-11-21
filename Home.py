import streamlit as st 
from PIL import Image 
import pandas as pd 

st.set_page_config(
	page_title="Coup du Monde APSIM", 
	page_icon="images/world-cup.png",
	initial_sidebar_state="expanded",
	layout="wide"
	)

st.markdown("<h1 style='text-align: center; color: navy blue;'>Prédiction Apsim de la coupe du monde 2022</h1>", unsafe_allow_html=True)
st.write("Veuillez ajouter votre pronostic pour le match!")


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

def submit(name, score1, score2): 
    submitButton = st.button("Envoyer 💸")
    df = pd.DataFrame()
    d = {'manager_name' : name, "score1" : score1, "score2": score2}
    
    if submitButton: 
        st.markdown("<h4>Merci pour votre réponse</h4>",unsafe_allow_html=True)
        df = df.append(d, ignore_index=True)
        open('results.csv', 'w').write(df.to_csv())


def main(): 
    name = st.text_area('Entrez votre nom', on_change=write_name, key='text_key')
    score1, score2 = show_country()
    submit(name,score1,score2)

if __name__ == "__main__": 
    main()
