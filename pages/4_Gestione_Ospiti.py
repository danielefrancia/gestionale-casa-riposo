import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("📋 Consultazione Ospiti")
conn = st.connection("gsheets", type=GSheetsConnection)

# Leggi dati
df = conn.read(worksheet="Ospiti", ttl=0)

# Visualizzazione
st.dataframe(df, use_container_width=True)

# Rimozione
st.divider()
st.subheader("❌ Rimuovi Ospite")
id_da_rimuovere = st.selectbox("Seleziona ID ospite da rimuovere", df['ID'].unique())

if st.button("Conferma Rimozione"):
    df_nuovo = df[df['ID'] != id_da_rimuovere]
    conn.update(worksheet="Ospiti", data=df_nuovo)
    st.warning(f"Ospite {id_da_rimuovere} rimosso. Aggiorna la pagina.")
