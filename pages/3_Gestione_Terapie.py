import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from fpdf import FPDF

# 1. Definisci la funzione di generazione (che hai già)
def genera_pdf(dataframe):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Report Terapie Giornaliere", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(60, 10, "Farmaco", border=1)
    pdf.cell(40, 10, "Orario", border=1)
    pdf.cell(40, 10, "Stato", border=1)
    pdf.ln()
    
    pdf.set_font("Arial", size=10)
    for i in dataframe.index:
        pdf.cell(60, 10, str(dataframe.loc[i, 'Farmaco']), border=1)
        pdf.cell(40, 10, str(dataframe.loc[i, 'Orario']), border=1)
        pdf.cell(40, 10, str(dataframe.loc[i, 'Stato']), border=1)
        pdf.ln()
    
    return pdf.output(dest='S').encode('latin-1')

# 2. CARICA I DATI NEL FILE ATTUALE
# Devi collegarti al database qui, esattamente come facevi in app.py
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(worksheet="Terapie") # Assicurati di mettere il nome corretto

# 3. Ora puoi chiamare la funzione in sicurezza
st.title("Gestione Terapie")
st.dataframe(df) # Esempio di visualizzazione

st.divider()

# Genera il PDF usando il 'df' appena caricato
pdf_bytes = genera_pdf(df)

st.download_button(
    label="📥 Scarica Report PDF",
    data=pdf_bytes,
    file_name="report_terapie.pdf",
    mime="application/pdf"
)
