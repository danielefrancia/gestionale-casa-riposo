import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.title("➕ Inserimento Nuovo Ospite")
conn = st.connection("gsheets", type=GSheetsConnection)

with st.form("form_ospiti", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        id_ospite = st.text_input("ID")
        giorno_ingresso = st.date_input("Giorno ingresso")
        nome = st.text_input("Nome")
        cognome = st.text_input("Cognome")
    with col2:
        data_nascita = st.date_input("Data nascita")
        camera = st.text_input("Camera")
        nome_fam = st.text_input("Nome Familiare")
        tel_fam = st.text_input("Tel familiare")
    note = st.text_area("Note")
    submitted = st.form_submit_button("Salva Ospite")

if submitted:
    nuovo_dato = pd.DataFrame([{
        "ID": id_ospite, "Nome": nome, "Cognome": cognome, 
        "Data nascita": str(data_nascita), "Camera": camera, 
        "Nome Familiare": nome_fam, "Tel familiare": tel_fam, "Note": note
    }])
    df_esistente = conn.read(worksheet="Ospiti")
    aggiornato = pd.concat([df_esistente, nuovo_dato], ignore_index=True)
    conn.update(worksheet="Ospiti", data=aggiornato)
    st.success("Ospite salvato!")
