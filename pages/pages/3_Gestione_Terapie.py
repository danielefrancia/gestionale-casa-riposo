import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.title("📋 Gestione Terapie")
conn = st.connection("gsheets", type=GSheetsConnection)

# Leggiamo i dati di ospiti e terapie
df_terapie = conn.read(worksheet="Terapie", ttl=0)
df_ospiti = conn.read(worksheet="Ospiti", ttl=0)

# Creiamo un menu per filtrare le terapie per ospite
lista_ospiti = df_ospiti['Nome'] + " " + df_ospiti['Cognome'] + " (ID: " + df_ospiti['ID'].astype(str) + ")"
ospite_filtro = st.selectbox("Filtra terapie per ospite", ["Tutti"] + list(lista_ospiti))

if ospite_filtro != "Tutti":
    id_selezionato = ospite_filtro.split("(ID: ")[1].replace(")", "")
    df_visualizzato = df_terapie[df_terapie['ID Ospite'].astype(str) == id_selezionato]
else:
    df_visualizzato = df_terapie

st.dataframe(df_visualizzato, use_container_width=True)

# Cancellazione Terapia
st.divider()
st.subheader("❌ Rimuovi Terapia")

# Creiamo un identificativo unico per la riga da rimuovere (es: Indice o Farmaco+Orario)
if not df_visualizzato.empty:
    idx_da_rimuovere = st.selectbox("Seleziona la riga della terapia da eliminare", df_visualizzato.index)
    
    if st.button("Elimina questa terapia"):
        # Rimuoviamo la riga dal dataframe originale
        df_terapie = df_terapie.drop(idx_da_rimuovere)
        conn.update(worksheet="Terapie", data=df_terapie)
        st.warning("Terapia rimossa correttamente!")
        st.rerun()
else:
    st.info("Nessuna terapia trovata per questo ospite.")
