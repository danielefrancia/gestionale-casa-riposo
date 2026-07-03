import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection # Fondamentale

st.title("➕ Aggiungi Nuovo Ospite")

# Dichiara esplicitamente il tipo di connessione
conn = st.connection("gsheets", type=GSheetsConnection)

# Leggiamo i dati esistenti
df_esistente = conn.read(worksheet="Ospiti", usecols=[0, 1, 2, 3], ttl=0)

with st.form("form_ospiti", clear_on_submit=True):
    nome = st.text_input("Nome")
    cognome = st.text_input("Cognome")
    camera = st.text_input("Camera")
    familiare = st.text_input("Contatto Familiare")
    submitted = st.form_submit_button("Salva Ospite")

if submitted:
    # Creiamo una riga che contiene TUTTE le colonne del foglio
    nuovo_dato = pd.DataFrame([{
        "ID": "",             # Lascialo vuoto o metti un numero
        "Nome": nome, 
        "Cognome": cognome, 
        "Data nascita": "",   # Aggiungi questa colonna
        "Camera": camera, 
        "Nome Familiare": familiare, # Deve corrispondere esattamente al testo nel foglio
        "Tel familiare": "",  # Aggiungi questa colonna
        "Note": ""            # Aggiungi questa colonna
    }])
    
    # ... resto del codice uguale
    
    # Uniamo
    aggiornato = pd.concat([df_esistente, nuovo_dato], ignore_index=True)
    
    # Questo è il comando corretto per sovrascrivere il foglio con la libreria st-gsheets-connection
    conn.update(worksheet="Ospiti", data=aggiornato)
    
    st.success(f"Ospite {nome} {cognome} salvato correttamente!")
