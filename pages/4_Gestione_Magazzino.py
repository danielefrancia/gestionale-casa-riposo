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

# 3. ANALISI SCORTE E DOWNLOAD
st.divider()
st.subheader("📊 Analisi e Download Inventario")

# Calcolo dello scarto dalla soglia
df_analisi = df_magazzino.copy()
# Calcoliamo quanto manca alla soglia (più è basso/negativo, più è urgente)
df_analisi['Differenza_Soglia'] = df_analisi['Quantità'] - df_analisi['Soglia_Minima']

# Ordinamento: le scorte più basse (o sotto soglia) vanno in alto
df_analisi = df_analisi.sort_values(by='Differenza_Soglia', ascending=True)

# Mostriamo l'anteprima ordinata
st.dataframe(df_analisi[['Nome_Farmaco', 'Quantità', 'Soglia_Minima', 'Differenza_Soglia']])

# Preparazione CSV per il download
csv = df_analisi.to_csv(index=False).encode('utf-8')

st.download_button(
    label="📥 Scarica Report Inventario (Ordinato per Urgenza)",
    data=csv,
    file_name="report_magazzino_urgente.csv",
    mime="text/csv"
)

# Logica per salvare modifiche
if st.button("Salva Modifiche"):
    conn.update(worksheet="Magazzino", data=df_magazzino)
    st.success("Magazzino aggiornato con successo!")
