import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.title("📋 Consultazione e Modifica Ospiti")
conn = st.connection("gsheets", type=GSheetsConnection)

# Leggiamo i dati sempre freschi
df = conn.read(worksheet="Ospiti", ttl=0)

# 1. Selezione ospite tramite menu
id_selezionato = st.selectbox("Seleziona ID ospite da modificare", df['ID'].unique())

if id_selezionato:
    # Filtriamo i dati dell'ospite scelto
    ospite_data = df[df['ID'] == id_selezionato].iloc[0]
    
    with st.form("form_modifica"):
        st.subheader(f"Modifica dati di {ospite_data['Nome']} {ospite_data['Cognome']}")
        
        # Campi pre-compilati con i dati attuali
        nuovo_nome = st.text_input("Nome", value=ospite_data['Nome'])
        nuovo_cognome = st.text_input("Cognome", value=ospite_data['Cognome'])
        nuova_camera = st.text_input("Camera", value=ospite_data['Camera'])
        nuovo_tel = st.text_input("Tel familiare", value=ospite_data['Tel familiare'])
        
        btn_salva = st.form_submit_button("Salva modifiche")

    if btn_salva:
        # Aggiorniamo il DataFrame
        df.loc[df['ID'] == id_selezionato, ['Nome', 'Cognome', 'Camera', 'Tel familiare']] = [
            nuovo_nome, nuovo_cognome, nuova_camera, nuovo_tel
        ]
        
        # Salviamo su Google Sheets
        conn.update(worksheet="Ospiti", data=df)
        st.success("Modifiche salvate con successo!")
        st.rerun()

# Visualizzazione tabella
st.divider()
st.dataframe(df, use_container_width=True)
