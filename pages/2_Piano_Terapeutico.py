import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.title("💊 Inserimento Piano Terapeutico")
conn = st.connection("gsheets", type=GSheetsConnection)

# Leggi ospiti e gestisci il caso in cui il foglio sia vuoto
df_ospiti = conn.read(worksheet="Ospiti", ttl=0)

if df_ospiti.empty:
    st.error("Nessun ospite trovato nel database. Inserisci prima un ospite nella pagina dedicata.")
    st.stop() # Ferma l'esecuzione della pagina

# Assicuriamoci che l'ID sia stringa
df_ospiti['ID'] = df_ospiti['ID'].astype(str)

# Creazione lista con controllo sui dati mancanti
lista_nomi = (df_ospiti['Nome'].fillna('') + " " + 
              df_ospiti['Cognome'].fillna('') + " (ID: " + 
              df_ospiti['ID'] + ")")

ospite_selezionato = st.selectbox("Seleziona Ospite", lista_nomi)

# Eseguiamo lo split solo se ospite_selezionato non è None
if ospite_selezionato and "(ID: " in ospite_selezionato:
    id_ospite = ospite_selezionato.split("(ID: ")[1].replace(")", "")
else:
    id_ospite = None

with st.form("form_terapia", clear_on_submit=True):
    farmaco = st.text_input("Nome Farmaco")
    dosaggio = st.text_input("Dosaggio")
    orario = st.time_input("Orario Somministrazione")
    note_terapia = st.text_area("Note")
    submitted = st.form_submit_button("Salva Terapia")

if submitted:
    if not id_ospite:
        st.error("Seleziona un ospite valido!")
    else:
        # Il resto del codice di salvataggio rimane uguale
        nuova_terapia = pd.DataFrame([{
            "ID Ospite": id_ospite,
            "Farmaco": farmaco,
            "Dosaggio": dosaggio,
            "Orario": str(orario),
            "Stato": "Da fare",
            "Note": note_terapia
        }])
        
        df_terapie = conn.read(worksheet="Terapie", ttl=0)
        aggiornato = pd.concat([df_terapie, nuova_terapia], ignore_index=True)
        conn.update(worksheet="Terapie", data=aggiornato)
        st.success("Terapia salvata!")
