import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from fpdf import FPDF

st.title("📄 Consultazione Piano Terapeutico")
conn = st.connection("gsheets", type=GSheetsConnection)

# 1. Carichiamo dati
df_terapie = conn.read(worksheet="Terapie", ttl=0)
df_ospiti = conn.read(worksheet="Ospiti", ttl=0)

# 2. Selezione Ospite
lista_ospiti = df_ospiti['Nome'] + " " + df_ospiti['Cognome'] + " (ID: " + df_ospiti['ID'].astype(str) + ")"
ospite_scelto = st.selectbox("Seleziona l'ospite per visualizzare il piano", lista_ospiti)

if ospite_scelto:
    id_ospite = ospite_scelto.split("(ID: ")[1].replace(")", "")
    
    # Filtriamo le terapie per l'ospite
    piano_ospite = df_terapie[df_terapie['ID Ospite'].astype(str) == id_ospite]
    
    if not piano_ospite.empty:
        st.subheader(f"Piano Terapeutico per {ospite_scelto}")
        st.dataframe(piano_ospite, use_container_width=True)
        
        # 3. Funzione Stampa/PDF
        def genera_pdf_ospite(df, nome_ospite):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt=f"Piano Terapeutico: {nome_ospite}", ln=True, align='C')
            pdf.ln(10)
            
            # Intestazione tabella
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(60, 10, "Farmaco", border=1)
            pdf.cell(40, 10, "Dosaggio", border=1)
            pdf.cell(40, 10, "Orario", border=1)
            pdf.ln()
            
            # Dati
            pdf.set_font("Arial", size=12)
            for i in df.index:
                pdf.cell(60, 10, str(df.loc[i, 'Farmaco']), border=1)
                pdf.cell(40, 10, str(df.loc[i, 'Dosaggio']), border=1)
                pdf.cell(40, 10, str(df.loc[i, 'Orario']), border=1)
                pdf.ln()
            return pdf.output(dest='S').encode('latin-1')

        # Pulsante Download PDF
        pdf_bytes = genera_pdf_ospite(piano_ospite, ospite_scelto)
        st.download_button(
            label="📥 Scarica Piano in PDF",
            data=pdf_bytes,
            file_name=f"Piano_Terapeutico_{id_ospite}.pdf",
            mime="application/pdf"
        )
    else:
        st.info("Nessuna terapia registrata per questo ospite.")
