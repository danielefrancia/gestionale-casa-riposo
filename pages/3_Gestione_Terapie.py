import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
from fpdf import FPDF

# 1. FUNZIONI DI SUPPORTO
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

def scarica_magazzino(nome_farmaco, quantita_da_scaricare=1):
    df_magazzino = conn.read(worksheet="Magazzino")
    
    if nome_farmaco in df_magazzino['Nome_Farmaco'].values:
        idx = df_magazzino[df_magazzino['Nome_Farmaco'] == nome_farmaco].index[0]
        nuova_quantita = df_magazzino.at[idx, 'Quantità'] - quantita_da_scaricare
        df_magazzino.at[idx, 'Quantità'] = nuova_quantita
        
        # Aggiorna il foglio Magazzino
        conn.update(worksheet="Magazzino", data=df_magazzino)
        
        if nuova_quantita <= df_magazzino.at[idx, 'Soglia_Minima']:
            st.warning(f"⚠️ Attenzione: scorta bassa per {nome_farmaco}!")

# 2. CARICAMENTO DATI
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(worksheet="Terapie")

# 3. LOGICA DI ORDINAMENTO
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

# 4. INTERFACCIA UTENTE
st.title("Gestione Terapie")
st.dataframe(df)

st.divider()
st.subheader("Conferma somministrazione terapia")

# Selezione terapia da confermare
farmaco_scelto = st.selectbox("Seleziona il farmaco somministrato:", df['Farmaco'].unique())

if st.button("✅ Esegui Terapia e Scarica Magazzino"):
    # Qui aggiungeresti la logica per segnare 'Eseguito' nel foglio 'Terapie'
    # Esempio logico:
    scarica_magazzino(farmaco_scelto)
    st.success(f"Terapia di {farmaco_scelto} registrata e magazzino aggiornato!")

# 5. DOWNLOAD PDF
pdf_bytes = genera_pdf(df)
st.download_button(
    label="📥 Scarica Report PDF",
    data=pdf_bytes,
    file_name="report_terapie.pdf",
    mime="application/pdf"
)
