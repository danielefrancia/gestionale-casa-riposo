import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("➕ Aggiungi Nuovo Ospite")

conn = st.connection("gsheets", type=GSheetsConnection)

with st.form("form_ospiti"):
    nome = st.text_input("Nome")
    cognome = st.text_input("Cognome")
    camera = st.text_input("Camera")
    familiare = st.text_input("Contatto Familiare")
    submitted = st.form_submit_button("Salva Ospite")

if submitted:
    nuovo_ospite = {"Nome": nome, "Cognome": cognome, "Camera": camera, "Nome_Familiare": familiare}
    # Qui aggiungiamo i dati al foglio "Ospiti"
    conn.update(worksheet="Ospiti", data=nuovo_ospite)
    st.success(f"Ospite {nome} {cognome} aggiunto con successo!")
