import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.title("➕ Aggiungi Nuovo Ospite")

conn = st.connection("gsheets", type=GSheetsConnection)

with st.form("form_ospiti"):
    nome = st.text_input("Nome")
    cognome = st.text_input("Cognome")
    camera = st.text_input("Camera")
    familiare = st.text_input("Contatto Familiare")
    submitted = st.form_submit_button("Salva Ospite")

if submitted:
    # Creiamo un DataFrame con i nuovi dati
    nuovo_dato = pd.DataFrame([{
        "Nome": nome, 
        "Cognome": cognome, 
        "Camera": camera, 
        "Nome_Familiare": familiare
    }])
    
    # Aggiungiamo i dati in coda al foglio "Ospiti"
    conn.append(worksheet="Ospiti", data=nuovo_dato)
    
    st.success(f"Ospite {nome} {cognome} salvato correttamente su Google Sheets!")
