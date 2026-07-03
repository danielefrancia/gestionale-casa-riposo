import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("📦 Gestione Magazzino")

# Connessione
conn = st.connection("gsheets", type=GSheetsConnection)

# Lettura dati
df_magazzino = conn.read(worksheet="Magazzino")

# Visualizzazione
st.subheader("Inventario Attuale")
st.data_editor(df_magazzino, use_container_width=True)

# Logica per salvare modifiche
if st.button("Salva Modifiche"):
    conn.update(worksheet="Magazzino", data=df_magazzino)
    st.success("Magazzino aggiornato con successo!")
