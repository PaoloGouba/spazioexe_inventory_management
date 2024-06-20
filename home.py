from modules.reparations import *
from modules.models import Reparation
from utils.tools import get_data, gen_recap

import streamlit as st
from streamlit_extras.row import row
from streamlit_extras.app_logo import add_logo
from streamlit_extras.card import card
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import time

st.set_page_config(
    page_icon="🧊",
    page_title="Spazio Exe - Riparazioni", 
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        "Get Help" : "https://www.osirisolutions.com/helpcenter/spazioexe/riparazioni",
        "Report a bug" : "mailto:support@osirisolutions.com"
    }
)

#@st.cache_data
def load_reparations_with_retries(max_retries=3, delay=2):
    for attempt in range(max_retries):
        try:
            return fetch_reparations(reparations_worksheet)
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
                raise e

df = load_reparations_with_retries()

#df = fetch_reparations(reparations_worksheet)


add_logo("img/logo.webp")

st.header('Riparazioni')

# Verifica la presenza delle colonne chiave
#required_columns = ['first_name', 'last_name', 'phone_number', 'device', 'brand', 'model', 'price', 'acconto', 'state', 'operator', 'unlock_code', 'color', 'action', 'url', 'muletto', 'left_accessory', 'descrizione_acessori_lasciati']
required_columns = ['Nome e Cognome']
missing_columns = [col for col in required_columns if col not in df.columns]

#st.write(df)

if missing_columns:
    st.error(f"Le seguenti colonne sono mancanti nel DataFrame: {', '.join(missing_columns)}")
else:

    with st.expander(label="Visualizza riparazioni"):
        selected_names = st.multiselect('Filtra per nome:', options=df['Nome e Cognome'].unique())

        filtered_df = df[
            (df['Nome e Cognome'].isin(selected_names) if selected_names else df['Nome e Cognome'].notnull())
        ]


        valori_indice = list(filtered_df.index)
        if len(valori_indice) != 0:

            sheet_line = st.selectbox('Seleziona la riparazione:', options=filtered_df.index.unique())
            final_sheet_df = filtered_df[(filtered_df.index.isin([sheet_line]) if sheet_line else filtered_df.index.notnull())]

        else :
            final_sheet_df = filtered_df

        try:
            st.write(final_sheet_df)
            row = final_sheet_df.iloc[0]
            request_date = row['Informazioni cronologiche']
            full_name = row['Nome e Cognome']
            phone_number = row['Numero di telefono']
            model = row['Dispositivo (Marca e Modello)']
            #device = row['Informazioni cronologiche']
            price = row['PREZZO (SCRIVERE SOLO IMPORTO) NO GARANZIA O ALTRO']
            acconto = row['ACCONTO (SCRIVERE SOLO IMPORTO) NO GARANZIA O ALTRO']
            #state = row['Informazioni cronologiche']
            #operator = row['Informazioni cronologiche']
            left_accessory = row['Accessori lasciati']
            unlock_code = row['Codice sblocco']
            color = row['Colore']
            action = row['Azione']
            url = row['Suggerimento di ordine (es. link fornitore)']
            muletto = row['Muletto']
            #descrizione_acessori_lasciati = row['Accessori lasciati'] + " --- " +  row['Accessori lasciati']
        
            download_input_data = {
                "request_date": request_date,
                "first_name": full_name,
                "last_name": "",
                "phone_number": phone_number,
                "device": "",
                "brand": "",
                "model": model,
                "price": price,
                "acconto": acconto,
                "state": "",
                "operator": "",
                "left_accessory": left_accessory,
                "unlock_code": unlock_code,
                "color": color,
                "action": action,
                "url": url,
                "muletto": muletto,
                "descrizione_acessori_lasciati": ""
            }

            gen_recap(download_input_data)

            with open("data/output.pdf", "rb") as file:
                btn = st.download_button(
                        label="Scarica PDF",
                        data=file,
                        file_name="output.pdf",
                        mime="application/pdf"
                    )

        except :
            st.info("Seleziona solo una scheda per poterla scaricare")
            #print(f"Key error: {e}")


        #except Exception as e:
        #    st.info(f"Scegli la riparazione da consultare: {str(e)}")

st.sidebar.markdown('<small>[Help Center](https://www.osirisolutions.com/helpcenter/spazioexe)</small>', unsafe_allow_html=True)
st.sidebar.markdown('<small>[Contact Us](mailto:paolo@osirisolutions.com)</small>', unsafe_allow_html=True)
st.sidebar.markdown('''<small>[Spazio Exe - Inventory Management v0.1](https://github.com/PaoloGouba/spazioexe_inventory_management)  | April 2024 | [Osiris Solutions](https://osirisolutions.com/)</small>''', unsafe_allow_html=True)
