import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
from fpdf import FPDF

# 1. DEFINIZIONE FUNZIONE (Mancava!)
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

# 2. Carica i dati
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(worksheet="Terapie")

# 3. Logica di ordinamento
df['Orario_dt'] = pd.to_datetime(df['Orario'], format='%H:%M:%S').dt.time
ora_attuale = datetime.now().time()

def calcola_distanza(orario_terapia):
    sec_terapia = orario_terapia.hour * 3600 + orario_terapia.minute * 60 + orario_terapia.second
    sec_attuale = ora_attuale.hour * 3600 + ora_attuale.minute * 60 + ora_attuale.second
    if sec_terapia < sec_attuale:
        return abs(sec_terapia - sec_attuale) + 86400 
    else:
        return sec_terapia - sec_attuale

df['distanza'] = df['Orario_dt'].apply(calcola_distanza)
df = df.sort_values(by='distanza').drop(columns=['distanza', 'Orario_dt'])

# 4. Visualizzazione e Download
st.title("Gestione Terapie")
st.dataframe(df)

pdf_bytes = genera_pdf(df)

st.divider()
st.download_button(
    label="📥 Scarica Report PDF",
    data=pdf_bytes,
    file_name="report_terapie.pdf",
    mime="application/pdf"
)
