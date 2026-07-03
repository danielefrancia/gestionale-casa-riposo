import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Configurazione pagina
st.set_page_config(page_title="Gestione Ospiti - Casa di Riposo", layout="wide")

# Connessione al database (Google Sheets)
conn = st.connection("gsheets", type=GSheetsConnection)

# Titolo principale
st.title("🏥 Dashboard Giornaliera")
st.write(f"Oggi è il: **{datetime.now().strftime('%d/%m/%Y')}**")

# Funzione per caricare i dati (usiamo i nomi dei fogli creati nello step 1)
def load_data():
    ospiti = conn.read(worksheet="Ospiti")
    terapie = conn.read(worksheet="Terapie")
    magazzino = conn.read(worksheet="Magazzino")
    return ospiti, terapie, magazzino

ospiti_df, terapie_df, magazzino_df = load_data()

# --- SEZIONE 1: TERAPIE DEL GIORNO ---
st.subheader("💊 Piano Terapeutico Odierno")

# Uniamo i dati delle terapie con i nomi degli ospiti per chiarezza
if not terapie_df.empty and not ospiti_df.empty:
    merged_df = pd.merge(terapie_df, ospiti_df[['ID', 'Nome', 'Cognome', 'Camera']], 
                         left_on='ID_Ospite', right_on='ID')
    
    # Visualizziamo solo le info necessarie per l'operatore
    display_terapie = merged_df[['Ora_Somministrazione', 'Nome', 'Cognome', 'Camera', 'Nome_Farmaco', 'Dosaggio']]
    st.table(display_terapie.sort_values(by='Ora_Somministrazione'))
else:
    st.info("Nessuna terapia registrata per oggi.")

# --- SEZIONE 2: SCADENZE MEDICINALI ---
st.divider()
st.subheader("⚠️ Avvisi Magazzino e Ordini")

low_stock = magazzino_df[magazzino_df['Quantità'] <= magazzino_df['Soglia_Minima']]

if not low_stock.empty:
    for _, row in low_stock.iterrows():
        st.error(f"**ORDINE NECESSARIO:** {row['Nome_Farmaco']} (Rimanenti: {row['Quantità']} - Soglia: {row['Soglia_Minima']})")
else:
    st.success("Tutte le scorte di medicinali sono adeguate.")

# Sidebar per navigazione rapida (la implementeremo nei prossimi step)
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3063/3063176.png", width=100)
st.sidebar.title("Menu")
st.sidebar.info("Usa le pagine laterali per gestire gli inserimenti.")
