import streamlit as st
from streamlit_extras.card import card
from streamlit_extras.app_logo import add_logo
from modules.devices import *
from modules.models import Device
from utils.tools import gen_recap
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(
    page_icon="🧊",
    page_title="Spazio Exe - Magazzino Dispositivi", 
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help" : "https://www.osirisolutions.com/helpcenter/spazioexe",
        "Report a bug" : "mailto:support@osirisolutions.com"
    }
)

@st.cache_data
def load_devices():
    return fetch_device(inventory_worksheet)

insights_df = load_devices()


add_logo("img/logo.webp")

st.header('Magazzino dispositivi')

col_1, col_2 = st.columns(2)

with col_1:
    with st.expander("Visualizza disponibilità"):
        st.caption("Filtra per:")
        selected_names = st.multiselect('Nome:', options=insights_df['customer_name'].unique())
        selected_last_names = st.multiselect('Cognome:', options=insights_df['customer_last_name'].unique())
        selected_devices = st.multiselect('Tipo di dispositivo:', options=insights_df['device_type'].unique())
        selected_brand = st.multiselect('Marca:', options=insights_df['brand'].unique())
        selected_state = st.multiselect('Stato:', options=insights_df['status'].unique())
        selected_imei = st.multiselect('Imei:', options=insights_df['imei_code'].unique())
        selected_grade = st.multiselect('Grado:', options=insights_df['grade'].unique())
        selected_capacity = st.multiselect('Memoria:', options=insights_df['capacity'].unique())
        selected_battery_health = st.multiselect('Stato Batteria:', options=insights_df['battery_health'].unique())

        filtered_df = insights_df[
            (insights_df['customer_name'].isin(selected_names) if selected_names else insights_df['customer_name'].notnull()) &
            (insights_df['customer_last_name'].isin(selected_last_names) if selected_last_names else insights_df['customer_last_name'].notnull()) &
            (insights_df['device_type'].isin(selected_devices) if selected_devices else insights_df['device_type'].notnull()) &
            (insights_df['brand'].isin(selected_brand) if selected_brand else insights_df['brand'].notnull()) & 
            (insights_df['status'].isin(selected_state) if selected_state else insights_df['status'].notnull()) & 
            (insights_df['imei_code'].isin(selected_imei) if selected_imei else insights_df['imei_code'].notnull()) &
            (insights_df['grade'].isin(selected_grade) if selected_grade else insights_df['grade'].notnull()) &
            (insights_df['capacity'].isin(selected_capacity) if selected_capacity else insights_df['capacity'].notnull()) &
            (insights_df['battery_health'].isin(selected_battery_health) if selected_battery_health else insights_df['battery_health'].notnull()) 
        ]

        st.caption('Lista dispositivi')
        st.dataframe(filtered_df)

        valori_indice = list(filtered_df.index)
        if len(valori_indice) == 1:
            st.write("Valori dell'indice:", valori_indice)
            if st.button("Elimina", type="secondary"):
                remove_device(inventory_worksheet, valori_indice[0] + 1)  # +1 perché l'indice del DataFrame parte da 0
                st.success(f"Dispositivo rimosso con successo dalla riga {valori_indice[0] + 1}")

    if len(filtered_df) == 1:
        try:
            for row in filtered_df.itertuples():
                device_type = row.device_type
                price = row.price
                sell_price = row.sell_price
                imei_code = row.imei_code
                battery_health = row.battery_health
                brand = row.brand
                model = row.model
                grade = row.grade
                capacity = row.capacity
                status = row.status
                manufacturer = row.manufacturer
                sold = row.sold
                customer_name = row.customer_name
                customer_last_name = row.customer_last_name
                selling_date = row.selling_date
                article_type = row.article_type

                c_text = f"{capacity} | {status} | {battery_health} | {sell_price}"

                card(
                    title=f"{device_type} | {brand} | {model} | {grade}",
                    text=c_text,
                    styles={
                        "card": {"background": "black"},
                        "text": {}
                    }
                )

                with st.expander("Più informazioni"):
                    st.caption("Ref #76989JIBI")

                    st.subheader("Informazioni Dispositivo")
                    st.write("Tipo di dispositivo: " + device_type)
                    st.write("Marca: " + brand)
                    st.write("Modello: " + model)
                    st.write("Manufacturer: " + manufacturer)
                    st.write("Prezzo: " + str(price))
                    st.write("Prezzo di vendita: " + str(sell_price))
                    st.write("IMEI: " + str(imei_code))
                    st.write("Stato batteria: " + str(battery_health))
                    st.write("Grado: " + grade)
                    st.write("Capacità: " + str(capacity))
                    st.write("Stato: " + status)

                    st.subheader("Informazioni Cliente")
                    st.write("Nome: " + customer_name)
                    st.write("Cognome: " + customer_last_name)

                    st.subheader("Altre informazioni")
                    st.write("Venduto: " + sold)
                    st.write("Data vendita: " + selling_date)
                    if type(article_type) is not str:
                        st.write("Articolo: " + str(article_type))
                    else:
                        st.write("Articolo: " + article_type)
        except Exception as e:
            st.error("Errore: " + str(e)) 

with col_2:
    with st.expander("Inserisci dispositivo"):
        if 'input_data' not in st.session_state:
            st.session_state['input_data'] = {
                'device_type': '',
                'price': 0.0,
                'sell_price': 0.0,
                'imei_code': '',
                'battery_health': '',
                'brand': '',
                'model': '',
                'grade': 'A',
                'capacity': '',
                'status': 'Nuovo',
                'manufacturer': '',
                'sold': False,
                'customer_name': '',
                'customer_last_name': '',
                'selling_date': '',
                'article_type': ''
            }

        with st.form("inserisci_dispositivo_form"):
            st.session_state['input_data']['device_type'] = st.selectbox("Tipo dispositivo", options=["TV", "PC", "Smartphone", "Tablet"], index=["TV", "PC", "Smartphone", "Tablet"].index(st.session_state['input_data']['device_type']))
            st.session_state['input_data']['price'] = st.number_input("Prezzo", min_value=0.0, format="%.2f", value=st.session_state['input_data']['price'])
            st.session_state['input_data']['sell_price'] = st.number_input("Prezzo di vendita", min_value=0.0, format="%.2f", value=st.session_state['input_data']['sell_price'])
            st.session_state['input_data']['imei_code'] = st.text_input("IMEI", value=st.session_state['input_data']['imei_code'])
            st.session_state['input_data']['battery_health'] = st.text_input("Batteria %", value=st.session_state['input_data']['battery_health'])
            st.session_state['input_data']['brand'] = st.text_input("Marca", value=st.session_state['input_data']['brand'])
            st.session_state['input_data']['model'] = st.text_input("Modello", value=st.session_state['input_data']['model'])
            st.session_state['input_data']['grade'] = st.selectbox("Grado", options=["A", "B", "C", "D", "Premium"], index=["A", "B", "C", "D", "Premium"].index(st.session_state['input_data']['grade']))
            st.session_state['input_data']['capacity'] = st.text_input("Capacità", value=st.session_state['input_data']['capacity'])
            st.session_state['input_data']['status'] = st.selectbox("Stato", options=["Nuovo", "Usato", "Ricondizionato"], index=["Nuovo", "Usato", "Ricondizionato"].index(st.session_state['input_data']['status']))
            st.session_state['input_data']['manufacturer'] = st.text_input("Produttore/Fabbricante", value=st.session_state['input_data']['manufacturer'])
            st.session_state['input_data']['sold'] = st.checkbox("Venduto", st.session_state['input_data']['sold'])
            st.session_state['input_data']['customer_name'] = st.text_input("Nome", value=st.session_state['input_data']['customer_name'])
            st.session_state['input_data']['customer_last_name'] = st.text_input("Cognome", value=st.session_state['input_data']['customer_last_name'])
            st.session_state['input_data']['selling_date'] = st.text_input("Data vendita", value=st.session_state['input_data']['selling_date'])
            st.session_state['input_data']['article_type'] = st.text_input("Tipo di articolo", value=st.session_state['input_data']['article_type'])

            submit_button = st.form_submit_button('Aggiungi')
            if submit_button:
                try:
                    device = Device(**st.session_state['input_data'])
                    add_device(inventory_worksheet, list(device.model_dump().values()))
                    st.success("Dispositivo aggiunto con successo!")
                except Exception as e:
                    st.error(f"Errore nella convalida dei dati: {str(e)}")

    with st.expander("Statistiche magazzino", expanded=True):
        insights_df.fillna(method='ffill', inplace=True)
        insights_df['selling_date'] = pd.to_datetime(insights_df['selling_date'])
        insights_df['sell_price'] = insights_df['sell_price'].astype(float)
        insights_df['price'] = insights_df['price'].astype(float)

        insights_df['Margine_profitto'] = insights_df['sell_price'] - insights_df['price']
        n_dispositivi_per_tipo = insights_df["device_type"].value_counts()
        for tipo_dispositivo, numero_dispositivi in n_dispositivi_per_tipo.items():
            print(f"- {tipo_dispositivo}: {numero_dispositivi}")
            
        plt.figure(figsize=(8, 6))
        n_dispositivi_per_tipo.plot(kind="bar", color=['tab:blue', 'tab:orange', 'tab:green', 'tab:purple'])
        plt.title("Distribuzione dei tipi di dispositivo in magazzino")
        plt.xlabel("Tipo di dispositivo")
        plt.ylabel("Numero di dispositivi")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        st.pyplot(plt)

        n_dispositivi_per_stato = insights_df["status"].value_counts()
        plt.figure(figsize=(8, 6))
        n_dispositivi_per_stato.plot(kind="bar")
        plt.title("Distribuzione degli stati dei dispositivi")
        plt.xlabel("Stato")
        plt.ylabel("Numero di dispositivi")
        st.pyplot(plt)

        n_dispositivi_per_brand = insights_df["brand"].value_counts()
        n_dispositivi_per_brand = n_dispositivi_per_brand.sort_values(ascending=False)
        top_10_brand = n_dispositivi_per_brand.head(10)

        plt.figure(figsize=(12, 6))
        top_10_brand.plot(kind="bar")
        plt.title("Top 10 brand con il maggior numero di dispositivi")
        plt.xlabel("Brand")
        plt.ylabel("Numero di dispositivi")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        st.pyplot(plt)

        n_dispositivi_per_grado = insights_df["grade"].value_counts()
        plt.figure(figsize=(8, 6))
        n_dispositivi_per_grado.plot(kind="pie", autopct="%1.1f%%")
        plt.title("Distribuzione dei gradi dei dispositivi")
        st.pyplot(plt)

        if 'status' in insights_df.columns:
            fig, ax = plt.subplots()
            insights_df['status'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax)
            ax.set_ylabel('')
            ax.set_title('Distribuzione dei Tipi di Dispositivo')
            st.pyplot(fig)
        else:
            st.error('La colonna "status" non è presente nel DataFrame. Verifica i dati.')

    with st.expander("Elimina dispositivo/i"):
        selected_index = st.selectbox("Seleziona l'ID della riga da rimuovere", range(len(insights_df)))
        if st.button('Rimuovi dispositivo'):
            remove_device(inventory_worksheet, selected_index + 1)
            st.success(f"Dispositivo rimosso con successo dalla riga {selected_index + 1}")

    with st.expander("Modifica scheda dispositivo"):
        def get_data():
            data = inventory_worksheet.get_all_records()
            return pd.DataFrame(data)

        df = get_data()
        filtro_stato = st.selectbox("Filtra per stato", ['Tutti'] + list(df['status'].unique()))
        if filtro_stato != 'Tutti':
            df = df[df['status'] == filtro_stato]

        st.write(df)

        selected_row_index = st.selectbox("Seleziona la riga da modificare:", df.index)
        selected_row = df.iloc[selected_row_index]

        with st.form("edit_form"):
            new_data = {
                'device_type': st.selectbox("Tipo dispositivo", options=["TV", "PC", "Smartphone", "Tablet"], index=["TV", "PC", "Smartphone", "Tablet"].index(selected_row['device_type'])),
                'price': st.number_input("Prezzo", value=selected_row['price'], format="%.2f"),
                'sell_price': st.number_input("Prezzo di vendita", value=selected_row['sell_price'], format="%.2f"),
                'imei_code': st.text_input("IMEI", value=selected_row['imei_code']),
                'battery_health': st.text_input("Batteria %", value=selected_row['battery_health']),
                'brand': st.text_input("Marca", value=selected_row['brand']),
                'model': st.text_input("Modello", value=selected_row['model']),
                'grade': st.selectbox("Grado", options=["A", "B", "C", "D", "Premium"], index=["A", "B", "C", "D", "Premium"].index(selected_row['grade'])),
                'capacity': st.text_input("Capacità", value=selected_row['capacity']),
                'status': st.selectbox("Stato", options=["Nuovo", "Usato", "Ricondizionato"], index=["Nuovo", "Usato", "Ricondizionato"].index(selected_row['status'])),
                'manufacturer': st.text_input("Produttore/Fabbricante", value=selected_row['manufacturer']),
                'sold': st.checkbox("Venduto", selected_row['sold']),
                'customer_name': st.text_input("Nome", value=selected_row['customer_name']),
                'customer_last_name': st.text_input("Cognome", value=selected_row['customer_last_name']),
                'selling_date': st.text_input("Data vendita", value=selected_row['selling_date']),
                'article_type': st.text_input("Tipo di articolo", value=selected_row['article_type'])
            }

            submit_button = st.form_submit_button("Salva Modifiche")
            if submit_button:
                try:
                    valid_data = Device(**new_data)
                    inventory_worksheet.update(f'A{selected_row_index + 2}:D{selected_row_index + 2}', [list(valid_data.dict().values())])
                    st.success("Modifiche salvate con successo!")
                except Exception as e:
                    st.error(f"Errore di validazione: {str(e)}")

                df = get_data()
                st.write(df)

st.sidebar.markdown('Spazio Exe - Inventory MGMT')
st.sidebar.markdown('<small>[Help Center](https://www.osirisolutions.com/helpcenter/spazioexe)</small>', unsafe_allow_html=True)
st.sidebar.markdown('<small>[Contact Us](mailto:paolo@osirisolutions.com)</small>', unsafe_allow_html=True)
st.sidebar.markdown('''<small>[Spazio Exe - Inventory Management v0.1](https://github.com/PaoloGouba/spazioexe_inventory_management)  | April 2024 | [Osiris Solutions](https://osirisolutions.com/)</small>''', unsafe_allow_html=True)
