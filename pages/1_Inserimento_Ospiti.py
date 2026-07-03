import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.title("➕ Aggiungi Nuovo Ospite")

conn = st.connection("gsheets", type=GSheetsConnection)

# Leggiamo i dati esistenti per mantenere la struttura
df_esistente = conn.read(worksheet="Ospiti")

with st.form("form_ospiti"):
    nome = st.text_input("Nome")
    cognome = st.text_input("Cognome")
    camera = st.text_input("Camera")
    familiare = st.text_input("Contatto Familiare")
    submitted = st.form_submit_button("Salva Ospite")

if submitted:
    # Creiamo una riga con i nuovi dati
    nuovo_dato = pd.DataFrame([{
        "Nome": nome, 
        "Cognome": cognome, 
        "Camera": camera, 
        "Nome_Familiare": familiare
    }])
    
    # Uniamo i vecchi dati ai nuovi
    aggiornato = pd.concat([df_esistente, nuovo_dato], ignore_index=True)
    
    # Sovrascriviamo il foglio con il nuovo DataFrame completo
    conn.write(worksheet="Ospiti", data=aggiornato)
    
    st.success(f"Ospite {nome} {cognome} salvato correttamente su Google Sheets!")
