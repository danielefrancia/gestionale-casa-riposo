import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# Configurazione Pagina Stile Clinico
st.set_page_config(page_title="Gestione Casa di Riposo", layout="wide")

# CSS per look professionale "clinico"
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    h1, h2, h3 { color: #2c3e50; font-family: sans-serif; }
    .stMetric { background-color: white; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; }
    </style>
""", unsafe_allow_html=True)

st.title("🏥 Dashboard Operativa - Clinica")

conn = st.connection("gsheets", type=GSheetsConnection)

# 1. Caricamento dati
df_terapie = conn.read(worksheet="Terapie", ttl=0)
df_ospiti = conn.read(worksheet="Ospiti", ttl=0)
df_mag = conn.read(worksheet="Magazzino", ttl=0)

# 2. Riepilogo Rapido (Stile Clinico con st.metric)
totale_terapie = len(df_terapie)
da_fare = len(df_terapie[df_terapie['Stato'] == "Da fare"])

col1, col2 = st.columns(2)
col1.metric("Totale Terapie Giornaliere", totale_terapie)
col2.metric("In Attesa di Somministrazione", da_fare)

st.divider()

# 3. Vista Odierna (Terapie da fare)
st.subheader("💊 Priorità di Oggi")

if not df_terapie.empty:
    da_fare_df = df_terapie[df_terapie['Stato'] == "Da fare"]
    
    if not da_fare_df.empty:
        da_fare_df = da_fare_df.merge(df_ospiti[['ID', 'Nome', 'Cognome']], left_on='ID Ospite', right_on='ID', how='left')
        st.dataframe(
            da_fare_df[['Nome', 'Cognome', 'Farmaco', 'Dosaggio', 'Orario']], 
            use_container_width=True, hide_index=True
        )
    else:
        st.success("✅ Tutte le terapie di oggi sono state somministrate.")
else:
    st.info("Nessuna terapia programmata.")

# 4. Alert Magazzino (Stile "Urgenza")
st.divider()
st.subheader("🚨 Monitoraggio Scorte (Alert Magazzino)")

df_urgenti = df_mag[df_mag['Quantità'] <= df_mag['Soglia_Minima']]

if not df_urgenti.empty:
    # Stile Clinico: Visualizzazione chiara dell'errore
    st.error("ATTENZIONE: Articoli sotto soglia minima")
    st.table(df_urgenti[['Nome_Farmaco', 'Quantità', 'Soglia_Minima']])
else:
    st.success("✅ Livelli di scorta ottimali.")

# 5. Navigazione Rapida Sidebar
st.sidebar.header("Navigazione Rapida")
st.sidebar.page_link("app.py", label="Dashboard", icon="🏠")
st.sidebar.page_link("pages/1_Inserimento_Ospiti.py", label="Nuovo Ospite", icon="➕")
st.sidebar.page_link("pages/2_Piano_Terapeutico.py", label="Nuova Terapia", icon="💊")
st.sidebar.page_link("pages/3_Gestione_Terapie.py", label="Gestione Terapie", icon="📋")
st.sidebar.page_link("pages/4_Gestione_Ospiti.py", label="Gestione Ospiti", icon="👤")
st.sidebar.page_link("pages/4_Gestione_Magazzino.py", label="Gestione Magazzino", icon="📦")
st.sidebar.info("Usa le pagine laterali per gestire gli inserimenti operativi.")
