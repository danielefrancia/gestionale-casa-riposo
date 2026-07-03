import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from fpdf import FPDF

# ... (il resto del tuo codice di lettura dati e gestione stato) ...

# Funzione per generare il PDF
def genera_pdf(dataframe):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Report Terapie Giornaliere", ln=True, align='C')
    pdf.ln(10) # Spazio dopo il titolo
    
    # Intestazione tabella nel PDF
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(60, 10, "Farmaco", border=1)
    pdf.cell(40, 10, "Orario", border=1)
    pdf.cell(40, 10, "Stato", border=1)
    pdf.ln()
    
    # Dati
    pdf.set_font("Arial", size=10)
    for i in dataframe.index:
        pdf.cell(60, 10, str(dataframe.loc[i, 'Farmaco']), border=1)
        pdf.cell(40, 10, str(dataframe.loc[i, 'Orario']), border=1)
        pdf.cell(40, 10, str(dataframe.loc[i, 'Stato']), border=1)
        pdf.ln()
    
    return pdf.output(dest='S').encode('latin-1')

# --- IL PULSANTE DOWNLOAD DEVE STARE FUORI DAGLI ALTRI IF ---
st.divider()
pdf_bytes = genera_pdf(df)
st.download_button(
    label="📥 Scarica Report PDF",
    data=pdf_bytes,
    file_name="report_terapie.pdf",
    mime="application/pdf"
)
