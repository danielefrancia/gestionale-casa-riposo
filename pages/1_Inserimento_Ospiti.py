import streamlit as st
import pandas as pd

st.title("➕ Aggiungi Nuovo Ospite")

# Connessione
conn = st.connection("gsheets")

# Leggiamo i dati esistenti
df_esistente = conn.read(worksheet="Ospiti", usecols=[0, 1, 2, 3], ttl=0)

with st.form("form_ospiti", clear_on_submit=True):
    nome = st.text_input("Nome")
    cognome = st.text_input("Cognome")
    camera = st.text_input("Camera")
    familiare = st.text_input("Contatto Familiare")
    submitted = st.form_submit_button("Salva Ospite")

if submitted:
    # Creiamo la nuova riga
    nuovo_dato = pd.DataFrame([{
        "Nome": nome, 
        "Cognome": cognome, 
        "Camera": camera, 
        "Nome_Familiare": familiare
    }])
    
    # Uniamo
    aggiornato = pd.concat([df_esistente, nuovo_dato], ignore_index=True)
    
    # Questo è il comando corretto per sovrascrivere il foglio con la libreria st-gsheets-connection
    conn.update(worksheet="Ospiti", data=aggiornato)
    
    st.success(f"Ospite {nome} {cognome} salvato correttamente!")
