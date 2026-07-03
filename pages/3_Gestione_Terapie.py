import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
from fpdf import FPDF

# ... (tua funzione genera_pdf rimane invariata) ...

# 1. Carica i dati
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(worksheet="Terapie")

# 2. LOGICA DI ORDINAMENTO DINAMICO
# Converti in tempo
df['Orario_dt'] = pd.to_datetime(df['Orario'], format='%H:%M:%S').dt.time
ora_attuale = datetime.now().time()

def calcola_distanza(orario_terapia):
    sec_terapia = orario_terapia.hour * 3600 + orario_terapia.minute * 60 + orario_terapia.second
    sec_attuale = ora_attuale.hour * 3600 + ora_attuale.minute * 60 + ora_attuale.second
    
    # Se l'orario è già passato oggi, aggiunge 86400 secondi per spostarlo in fondo
    if sec_terapia < sec_attuale:
        return abs(sec_terapia - sec_attuale) + 86400 
    else:
        return sec_terapia - sec_attuale

# Applica l'ordinamento
df['distanza'] = df['Orario_dt'].apply(calcola_distanza)
df = df.sort_values(by='distanza').drop(columns=['distanza', 'Orario_dt'])

# 3. Ora df è ordinato correttamente
st.title("Gestione Terapie")
st.dataframe(df)

# --- CODICE PULITO E CORRETTO ---

# 1. Calcola il PDF una sola volta
pdf_bytes = genera_pdf(df)

# 2. Crea il pulsante di download una sola volta
st.divider()
st.download_button(
    label="📥 Scarica Report PDF",
    data=pdf_bytes,
    file_name="report_terapie.pdf",
    mime="application/pdf"
)
