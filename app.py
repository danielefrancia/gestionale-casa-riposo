import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

st.set_page_config(page_title="Gestione Casa di Riposo", layout="wide")
st.title("🏠 Dashboard Operativa")

conn = st.connection("gsheets", type=GSheetsConnection)

# 1. Caricamento dati
df_terapie = conn.read(worksheet="Terapie", ttl=0)
df_ospiti = conn.read(worksheet="Ospiti", ttl=0)

# 2. Riepilogo Rapido
col1, col2 = st.columns(2)
totale_terapie = len(df_terapie)
da_fare = len(df_terapie[df_terapie['Stato'] == "Da fare"])

col1.metric("Totale Terapie", totale_terapie)
col2.metric("Terapie da Somministrare", da_fare, delta_color="inverse")

st.divider()

# 3. Vista Odierna (Terapie da fare)
st.subheader("💊 Priorità di Oggi")

if not df_terapie.empty:
    # Filtriamo solo quelle "Da fare"
    da_fare_df = df_terapie[df_terapie['Stato'] == "Da fare"]
    
    if not da_fare_df.empty:
        # Uniamo con i nomi degli ospiti per chiarezza
        da_fare_df = da_fare_df.merge(df_ospiti[['ID', 'Nome', 'Cognome']], left_on='ID Ospite', right_on='ID', how='left')
        
        st.dataframe(
            da_fare_df[['Nome', 'Cognome', 'Farmaco', 'Dosaggio', 'Orario']], 
            use_container_width=True,
            hide_index=True
        )
    else:
        st.success("Tutte le terapie di oggi sono state somministrate!")
else:
    st.info("Nessuna terapia programmata.")

# --- LOGICA URGENZA MAGAZZINO ---
st.subheader("🚨 Alert Magazzino: Articoli in esaurimento")

# Leggi il magazzino
df_mag = conn.read(worksheet="Magazzino")

# Filtra solo gli articoli dove la quantità è <= soglia minima
df_urgenti = df_mag[df_mag['Quantità'] <= df_mag['Soglia_Minima']]

if not df_urgenti.empty:
    # Mostra gli articoli critici
    st.error("I seguenti articoli necessitano di un ordine immediato:")
    st.table(df_urgenti[['Nome_Farmaco', 'Quantità', 'Soglia_Minima']])
else:
    st.success("✅ Tutte le scorte sono sufficienti.")
    

# 4. Accesso Rapido
st.sidebar.header("Navigazione Rapida")
st.sidebar.page_link("app.py", label="Dashboard")
st.sidebar.page_link("pages/1_Inserimento_Ospiti.py", label="Nuovo Ospite")
st.sidebar.page_link("pages/2_Piano_Terapeutico.py", label="Nuova Terapia")
st.sidebar.page_link("pages/3_Gestione_Terapie.py", label="Gestione Terapie")
st.sidebar.page_link("pages/4_Gestione_Ospiti.py", label="Gestione Ospiti")
st.sidebar.info("Usa le pagine laterali per gestire gli inserimenti.")
