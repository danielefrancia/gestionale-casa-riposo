import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.title("💊 Inserimento Piano Terapeutico")
conn = st.connection("gsheets", type=GSheetsConnection)

# 1. Carichiamo la lista ospiti per il menu a tendina
df_ospiti = conn.read(worksheet="Ospiti", ttl=0)
# Creiamo una lista di nomi per la selezione
lista_nomi = df_ospiti['Nome'] + " " + df_ospiti['Cognome'] + " (ID: " + df_ospiti['ID'].astype(str) + ")"

with st.form("form_terapia", clear_on_submit=True):
    ospite_selezionato = st.selectbox("Seleziona Ospite", lista_nomi)
    farmaco = st.text_input("Nome Farmaco")
    dosaggio = st.text_input("Dosaggio (es. 10mg)")
    orario = st.time_input("Orario Somministrazione")
    note_terapia = st.text_area("Note aggiuntive")
    
    submitted = st.form_submit_button("Salva Terapia")

if submitted:
    # Estraiamo l'ID dall'ospite selezionato
    id_ospite = ospite_selezionato.split("(ID: ")[1].replace(")", "")
    
    nuova_terapia = pd.DataFrame([{
        "ID Ospite": id_ospite,
        "Farmaco": farmaco,
        "Dosaggio": dosaggio,
        "Orario": str(orario),
        "Note": note_terapia
    }])
    
    # Salvataggio su foglio "Terapie"
    df_terapie = conn.read(worksheet="Terapie", ttl=0)
    aggiornato = pd.concat([df_terapie, nuova_terapia], ignore_index=True)
    conn.update(worksheet="Terapie", data=aggiornato)
    st.success(f"Terapia per {ospite_selezionato} salvata!")
