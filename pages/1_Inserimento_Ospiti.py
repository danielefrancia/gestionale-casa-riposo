import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.title("➕ Inserimento Nuovo Ospite")
conn = st.connection("gsheets", type=GSheetsConnection)

# Leggiamo i dati per calcolare l'ID successivo
df = conn.read(worksheet="Ospiti", ttl=0)
# Assicuriamoci che l'ID sia numerico
df['ID'] = pd.to_numeric(df['ID'], errors='coerce')
prossimo_id = int(df['ID'].max() + 1) if not df['ID'].dropna().empty else 1

with st.form("form_ospiti", clear_on_submit=True):
    # ID in sola lettura
    st.text_input("ID (Generato automaticamente)", value=str(prossimo_id), disabled=True)
    
    giorno_ingresso = st.date_input("Giorno ingresso")
    nome = st.text_input("Nome")
    cognome = st.text_input("Cognome")
    data_nascita = st.date_input("Data nascita")
    camera = st.text_input("Camera")
    nome_fam = st.text_input("Nome Familiare")
    tel_fam = st.text_input("Tel familiare")
    note = st.text_area("Note")
    submitted = st.form_submit_button("Salva Ospite")

if submitted:
    nuovo_dato = pd.DataFrame([{
        "ID": prossimo_id, "Giorno ingresso": str(giorno_ingresso), "Nome": nome, "Cognome": cognome, 
        "Data nascita": str(data_nascita), "Camera": camera, 
        "Nome Familiare": nome_fam, "Tel familiare": tel_fam, "Note": note
    }])
    aggiornato = pd.concat([df, nuovo_dato], ignore_index=True)
    conn.update(worksheet="Ospiti", data=aggiornato)
    st.success(f"Ospite salvato con ID {prossimo_id}!")
