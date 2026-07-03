import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.title("📋 Consultazione, Modifica e Cancellazione")
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(worksheet="Ospiti", ttl=0)

id_selezionato = st.selectbox("Seleziona ID ospite", df['ID'].unique())

if id_selezionato:
    df_filtrato = df[df['ID'] == id_selezionato]
    if not df_filtrato.empty:
        ospite = df_filtrato.iloc[0]
        
        # Form di modifica
        with st.form("modifica_form"):
            nuovo_nome = st.text_input("Nome", value=str(ospite['Nome']))
            # ... (aggiungi qui gli altri campi che vuoi modificare)
            if st.form_submit_button("Salva Modifiche"):
                df.loc[df['ID'] == id_selezionato, 'Nome'] = nuovo_nome
                conn.update(worksheet="Ospiti", data=df)
                st.rerun()

        # Pulsante Cancellazione
        if st.button("⚠️ CANCELLA OSPITE DEFINITIVAMENTE"):
            df_pulito = df[df['ID'] != id_selezionato]
            conn.update(worksheet="Ospiti", data=df_pulito)
            st.warning("Ospite rimosso dal database.")
            st.rerun()

st.dataframe(df, use_container_width=True)
