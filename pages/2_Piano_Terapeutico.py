import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.title("💊 Inserimento Piano Terapeutico")
conn = st.connection("gsheets", type=GSheetsConnection)

# Leggi ospiti
df_ospiti = conn.read(worksheet="Ospiti", ttl=0)
# Assicuriamoci che l'ID sia stringa per evitare errori
df_ospiti['ID'] = df_ospiti['ID'].astype(str)

lista_nomi = df_ospiti['Nome'] + " " + df_ospiti['Cognome'] + " (ID: " + df_ospiti['ID'] + ")"

with st.form("form_terapia", clear_on_submit=True):
    ospite_selezionato = st.selectbox("Seleziona Ospite", lista_nomi)
    farmaco = st.text_input("Nome Farmaco")
    dosaggio = st.text_input("Dosaggio")
    orario = st.time_input("Orario Somministrazione")
    note_terapia = st.text_area("Note")
    submitted = st.form_submit_button("Salva Terapia")

if submitted:
    # Estraiamo l'ID correttamente
    id_ospite = ospite_selezionato.split("(ID: ")[1].replace(")", "")
    
    # Prepariamo la riga con i nomi identici al foglio pulito
    nuova_terapia = pd.DataFrame([{
        "ID Ospite": id_ospite,
        "Farmaco": farmaco,
        "Dosaggio": dosaggio,
        "Orario": str(orario),
        "Stato": "Da fare",
        "Note": note_terapia
    }])
    
    # Leggi terapie attuali
    df_terapie = conn.read(worksheet="Terapie", ttl=0)
    
    # Unisci
    aggiornato = pd.concat([df_terapie, nuova_terapia], ignore_index=True)
    
    # Salva
    conn.update(worksheet="Terapie", data=aggiornato)
    st.success("Terapia salvata!")
