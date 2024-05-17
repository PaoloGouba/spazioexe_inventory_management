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

@st.cache_data
def load_reparations():
    return fetch_reparations(reparations_worksheet)

df = load_reparations()



add_logo("img/logo.webp")

from streamlit_modal import Modal
import streamlit.components.v1 as components

st.header('Riparazioni')

col_1, col_2 = st.columns(2)

with col_2: 

    with st.expander("Nuova riparazione"):
        st.caption("Riparazione #C00001")

        if 'input_data' not in st.session_state:
            st.session_state['input_data'] = {
                'first_name': '',
                'last_name': '',
                'phone_number': '',
                'device': 'TV',
                'brand': '',
                'model': '',
                'price': 1.00,
                'acconto': '',
                'operator': '',
                'unlock_code': '',
                'color': '',
                'action': '',
                'url': '',
                'muletto': False,
                'left_accessory': False,
                'descrizione_acessory_lasciati': ''
            }

        with st.form("nuova_riparazione_form"):
            st.session_state['input_data']['first_name'] = st.text_input("Nome", st.session_state['input_data']['first_name'])
            st.session_state['input_data']['last_name'] = st.text_input("Cognome", st.session_state['input_data']['last_name'])
            st.session_state['input_data']['phone_number'] = st.text_input("Numero di telefono", st.session_state['input_data']['phone_number'])
            st.session_state['input_data']['device'] = st.selectbox("Tipo dispositivo", options=["TV", "PC", "Smartphone", "Tablet"], index=["TV", "PC", "Smartphone", "Tablet"].index(st.session_state['input_data']['device']))
            st.session_state['input_data']['brand'] = st.text_input("Marca", st.session_state['input_data']['brand'])
            st.session_state['input_data']['model'] = st.text_input("Modello", st.session_state['input_data']['model'])
            st.session_state['input_data']['price'] = st.number_input("Prezzo", value=st.session_state['input_data']['price'], format="%.2f", min_value=1.00)
            st.session_state['input_data']['acconto'] = st.text_input("Acconto", st.session_state['input_data']['acconto'])
            st.session_state['input_data']['operator'] = st.text_input("Operatore", st.session_state['input_data']['operator'])
            st.session_state['input_data']['unlock_code'] = st.text_input("Codice sblocco", st.session_state['input_data']['unlock_code'])
            st.session_state['input_data']['color'] = st.text_input("Colore", st.session_state['input_data']['color'])
            st.session_state['input_data']['action'] = st.text_input("Azione", st.session_state['input_data']['action'])
            st.session_state['input_data']['url'] = st.text_input("Link", st.session_state['input_data']['url'])
            st.session_state['input_data']['muletto'] = str(st.checkbox("Muletto", st.session_state['input_data']['muletto']))
            st.session_state['input_data']['left_accessory'] = str(st.checkbox("Accessori lasciati", st.session_state['input_data']['left_accessory']))

            if st.session_state['input_data']['left_accessory']:
                st.session_state['input_data']['descrizione_acessory_lasciati'] = st.text_input("Info accessori lasciati", st.session_state['input_data']['descrizione_acessory_lasciati'])
            
            submit_button = st.form_submit_button(label='Aggiungi riparazione')
            if submit_button:
                try:
                    reparation = Reparation(**st.session_state['input_data'])
                    add_reparation(reparations_worksheet, list(reparation.model_dump().values()))
                    temp_file_name = "Reparation_" + st.session_state['input_data']['first_name'] + ".pdf"
                    file_download_name = gen_recap(st.session_state['input_data'], temp_file_name)
                    st.success("Reparation aggiunta con successo!")
                except Exception as e:
                    st.error(f"Errore nella convalida dei dati: {str(e)}")

    with st.expander("Statistiche riparazioni", expanded=True):

        if 'price' in df.columns and 'brand' in df.columns and 'state' in df.columns and not df.empty:
            st.subheader("Totale riparazioni: " + str(len(df)), divider=True)

            orders_by_state = df['state'].value_counts()
            st.subheader("Riparazioni per stato:")
            plt.figure(figsize=(10, 6))
            sns.barplot(x=orders_by_state.index, y=orders_by_state.values)
            plt.xlabel('Stato')
            plt.ylabel('Numero Ordini')
            plt.title('Distribuzione degli ordini per stato')
            plt.xticks(rotation=45)
            st.pyplot(plt)
            for state, count in orders_by_state.items():
                st.write(f" - {state}: {count} items")

            popular_brands = df['brand'].value_counts().head(5)
            st.subheader("I 5 Brand più riparati:")
            plt.figure(figsize=(8, 8))
            plt.pie(popular_brands.values, labels=popular_brands.index, autopct='%1.1f%%')
            plt.title('Top 5 Popular Brands')
            st.pyplot(plt)
            i = 1
            for brand, count in popular_brands.items():
                st.write(f"{str(i)}. {brand}: {count} items")
                i += 1

    with st.expander("Modifica riparazione"):
        df = get_data(reparations_worksheet)
        filtro_stato = st.selectbox("Filtra per stato", ['Tutti'] + list(df['state'].unique()))
        if filtro_stato != 'Tutti':
            df = df[df['state'] == filtro_stato]

        st.write(df)

        selected_row_index = st.selectbox("Seleziona la riga da modificare:", df.index)
        selected_row = df.iloc[selected_row_index]

        with st.form("edit_form"):
            new_data = {
                'first_name': st.text_input("Nome", selected_row['first_name']),
                'last_name': st.text_input("Cognome", selected_row['last_name']),
                'phone_number': st.text_input("Numero di telefono", selected_row['phone_number']),
                'device': st.selectbox("Tipo dispositivo", options=["TV", "PC", "Smartphone", "Tablet"], index=["TV", "PC", "Smartphone", "Tablet"].index(selected_row['device'])),
                'brand': st.text_input("Marca", selected_row['brand']),
                'model': st.text_input("Modello", selected_row['model']),
                'price': st.text_input("Prezzo", selected_row['price']),
                'state': st.selectbox("Stato", options=["Consegnato", "In attesa", "Chiamato", "Annullato", "In sospeso"], index=["Consegnato", "In attesa", "Chiamato", "Annullato", "In sospeso"].index(selected_row['state'])),
                'operator': st.text_input("Operatore", selected_row['operator']),
                'unlock_code': st.text_input("Codice sblocco", selected_row['unlock_code']),
                'color': st.text_input("Colore", selected_row['color']),
                'action': st.text_input("Azione", selected_row['action']),
                'url': st.text_input("Link", selected_row['url']),
                'muletto': st.checkbox("Muletto", selected_row['muletto']),
                'left_accessory': st.checkbox("Accessori lasciati", selected_row['left_accessory'])
            }

            submit_button = st.form_submit_button("Salva Modifiche")
            if submit_button:
                try:
                    valid_data = Reparation(**new_data)
                    reparations_worksheet.update(f'A{selected_row_index + 2}:D{selected_row_index + 2}', [list(valid_data.dict().values())])
                    st.success("Modifiche salvate con successo!")
                except Exception as e:
                    st.error(f"Errore di validazione: {str(e)}")

                df = get_data(reparations_worksheet)
                st.write(df)

with col_1:
    with st.expander(label="Visualizza riparazioni"):
        selected_names = st.multiselect('Filtra per nome:', options=df['first_name'].unique())
        selected_last_names = st.multiselect('Filtra per cognome:', options=df['last_name'].unique())
        selected_devices = st.multiselect('Filtra per tipo di dispositivo:', options=df['device'].unique())
        selected_brand = st.multiselect('Filtra per Marca:', options=df['brand'].unique())
        selected_state = st.multiselect('Filtra per stato:', options=df['state'].unique())
        selected_action = st.multiselect('Filtra per azione:', options=df['action'].unique())

        filtered_df = df[
            (df['first_name'].isin(selected_names) if selected_names else df['first_name'].notnull()) &
            (df['last_name'].isin(selected_last_names) if selected_last_names else df['last_name'].notnull()) &
            (df['device'].isin(selected_devices) if selected_devices else df['device'].notnull()) &
            (df['brand'].isin(selected_brand) if selected_brand else df['brand'].notnull()) & 
            (df['state'].isin(selected_state) if selected_state else df['state'].notnull()) & 
            (df['action'].isin(selected_action) if selected_action else df['action'].notnull())
        ]
        st.caption('Lista riparazioni')
        st.dataframe(filtered_df)

        valori_indice = list(filtered_df.index)
        if len(valori_indice) == 1:
            print("Valori dell'indice:", valori_indice)

            if st.button("Elimina", type="secondary"):
                st.write(f"Sei sicuro di vole eliminare questa scheda?")
                if st.button("Elimina scheda"):
                    remove_reparation(reparations_worksheet, valori_indice[0] + 1)
                    st.success(f"Reparation rimossa con successo dalla riga {valori_indice[0] + 1}")

    if len(filtered_df) == 1:
        try:
            for row in filtered_df.itertuples():
                request_date = row.request_date
                first_name = row.first_name
                last_name = row.last_name
                phone_number = row.phone_number
                device = row.device
                brand = row.brand
                model = row.model
                price = row.price
                acconto = row.acconto
                state = row.state
                operator = row.operator
                left_accessory = row.left_accessory
                unlock_code = row.unlock_code
                color = row.color
                action = row.action
                url = row.url
                muletto = row.muletto
                descrizione_acessori_lasciati = row.descrizione_acessori_lasciati

                c_text = f"Cliente : {first_name} {last_name}\nAzione : {action}"

                card(
                    title=f"{device} - {brand} - {state}",
                    text=c_text,
                    styles={
                            "card": {"background" : "black"},
                            "text": {}
                            }
                    )

                download_input_data = {
                    "request_date": request_date,
                    "first_name": first_name,
                    "last_name": last_name,
                    "phone_number": phone_number,
                    "device": device,
                    "brand": brand,
                    "model": model,
                    "price": price,
                    "acconto": acconto,
                    "state": state,
                    "operator": operator,
                    "left_accessory": left_accessory,
                    "unlock_code": unlock_code,
                    "color": color,
                    "action": action,
                    "url": url,
                    "muletto": muletto,
                    "descrizione_acessori_lasciati": descrizione_acessori_lasciati
                }

                gen_recap(download_input_data)

                with open("data/output.pdf", "rb") as file:
                    btn = st.download_button(
                            label="Scarica PDF",
                            data=file,
                            file_name="output.pdf",
                            mime="application/pdf"
                        )

                with st.expander("Più informazioni"):
                    st.caption("Ref #76989JIBI")
                    st.write(f"Data Richiesta: {request_date}")
                    st.subheader("Informazioni Cliente")
                    st.write(f"Nome: {first_name}")
                    st.write(f"Cognome: {last_name}")
                    st.write(f"Telefono: {phone_number}")
                    st.subheader(f"Azione: {action}")
                    st.subheader("Informazioni Dispositivo")
                    st.write(f"Dispositivo: {device}")
                    st.write(f"Marca: {brand}")
                    st.write(f"Modello: {model}")
                    st.write(f"Prezzo: {price} EURO")
                    st.write(f"Acconto: {acconto} EURO")
                    st.write(f"Condizione: {state}")
                    st.write(f"Colore: {color}")
                    st.subheader("Altre informazioni")
                    st.write(f"Operatore: {operator}")
                    st.write(f"Accessorio lasciato: {left_accessory} | {descrizione_acessori_lasciati}")
                    st.write(f"Codice sblocco: {unlock_code}")
                    st.write(f"URL: {url}")
                    st.write(f"Muletto: {muletto}")

        except Exception as e:
            st.info(f"Scegli la riparazione da consultare: {str(e)}") 

st.sidebar.markdown('<small>[Help Center](https://www.osirisolutions.com/helpcenter/spazioexe)</small>', unsafe_allow_html=True)
st.sidebar.markdown('<small>[Contact Us](mailto:paolo@osirisolutions.com)</small>', unsafe_allow_html=True)
st.sidebar.markdown('''<small>[Spazio Exe - Inventory Management v0.1](https://github.com/PaoloGouba/spazioexe_inventory_management)  | April 2024 | [Osiris Solutions](https://osirisolutions.com/)</small>''', unsafe_allow_html=True)
