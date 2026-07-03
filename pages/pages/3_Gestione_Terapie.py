import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.title("📋 Gestione e Stato Terapie")
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read(worksheet="Terapie", ttl=0)

# Selezione terapia da aggiornare
idx_da_aggiornare = st.selectbox("Seleziona la terapia da gestire", df.index, format_func=lambda x: f"{df.loc[x, 'Farmaco']} - {df.loc[x, 'Orario']}")

col1, col2 = st.columns(2)
with col1:
    nuovo_stato = st.selectbox("Cambia Stato", ["Da fare", "Somministrato"])
with col2:
    if st.button("Aggiorna Stato"):
        df.loc[idx_da_aggiornare, 'Stato'] = nuovo_stato
        conn.update(worksheet="Terapie", data=df)
        st.success("Stato aggiornato!")
        st.rerun()

st.dataframe(df, use_container_width=True)
