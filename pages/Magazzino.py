import streamlit as st
from streamlit_extras.card import card
from streamlit_extras.sandbox import sandbox
from streamlit_extras.app_logo import add_logo
from modules.devices import *
from modules.models import Device
from utils.tools import gen_recap
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

insights_df = fetch_device(inventory_worksheet)

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

add_logo("img/logo.webp")

st.header('Magazzino dispositivi')

col_1, col_2 = st.columns(2)

with col_1:

    with st.expander("Visualizza disponibilità") :
        st.caption("Fitra per :")
        selected_names = st.multiselect('Nome:', options=insights_df['customer_name'].unique())
        selected_last_names = st.multiselect('Cognome:', options=insights_df['customer_last_name'].unique())
        selected_devices = st.multiselect('Tipo di dispositivo:', options=insights_df['device_type'].unique())
        selected_brand = st.multiselect('Marca:', options=insights_df['brand'].unique())
        selected_state = st.multiselect('Stato:', options=insights_df['status'].unique())
        selected_action = st.multiselect('Imei:', options=insights_df['imei_code'].unique())
        selected_action = st.multiselect('Grado:', options=insights_df['grade'].unique())
        selected_action = st.multiselect('Memoria:', options=insights_df['capacity'].unique())
        selected_action = st.multiselect('Stato Batteria:', options=insights_df['battery_health'].unique())


        filtered_df = insights_df[
            (insights_df['customer_name'].isin(selected_names) if selected_names else insights_df['customer_name'].notnull()) &
            (insights_df['customer_last_name'].isin(selected_last_names) if selected_last_names else insights_df['customer_last_name'].notnull()) &
            (insights_df['device_type'].isin(selected_devices) if selected_devices else insights_df['device_type'].notnull()) &
            (insights_df['brand'].isin(selected_brand) if selected_brand else insights_df['brand'].notnull()) & 
            (insights_df['status'].isin(selected_state) if selected_state else insights_df['status'].notnull()) & 
            (insights_df['imei_code'].isin(selected_action) if selected_action else insights_df['imei_code'].notnull()) &
            (insights_df['grade'].isin(selected_action) if selected_action else insights_df['grade'].notnull()) &
            (insights_df['capacity'].isin(selected_action) if selected_action else insights_df['capacity'].notnull()) &
            (insights_df['battery_health'].isin(selected_action) if selected_action else insights_df['battery_health'].notnull()) 

        ]
        st.caption('Lista riparazioni')
        # Mostra il DataFrame filtrato
        st.dataframe(filtered_df)


        valori_indice = list(filtered_df.index)
        if len(valori_indice) == 1 :
            st.write("Valori dell'indice:", valori_indice)
            if st.button("Elimina", type="secondary") :
                remove_device(inventory_worksheet, valori_indice[0] + 1)  # +1 perché l'indice del DataFrame parte da 0
                st.success(f"Reparation rimossa con successo dalla riga {valori_indice[0] + 1}")


   
    try :
        i = 0
        for row in filtered_df.itertuples():
            i=i+1

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

            c_text : str = f"{capacity} | {status} | {battery_health} | {sell_price}"

            card(
                title=f"{device_type} | {brand} | {model} | {grade}",
                text=c_text,
                styles={
                        "card": {
                            "background" : "black",
                            #"width": "500px",
                            #"height": "500px",
                            #"border-radius": "60px",
                            #"box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                                },
                        "text": {
                            #"font-family": "serif",
                                }
                        }
                )

            download_input_data = {
                "request_date" : "",
                "first_name" : customer_name,
                "last_name" : customer_last_name,
                "phone_number" : "",
                "device" : device_type,
                "brand" : brand,
                "model" : model,
                "price" : sell_price,
                "state" : f"",
                "operator" : "",
                "left_accessory" : "",
                "unlock_code" : "",
                "color" : "",
                "action" : "",
                "url" : "",
                "muletto" : ""
            }


            gen_recap(download_input_data)

            with open("data/output.pdf", "rb") as file:
                btn = st.download_button(
                        label="Scarica PDF",
                        data=file,
                        file_name="output.pdf",
                        mime="application/pdf"
                    )

            with st.expander("Più informazioni") :
                st.caption("Ref #76989JIBI") # dinamizzare

                st.subheader("Informazioni Dispositivo")
                st.write("Typo di dispositivo : " + device_type)
                st.write("Marca : " + brand)
                st.write("Modello : " + model)
                st.write("Manufacturer : " + manufacturer)
                st.write("Prezzo : " + str(price))
                st.write("Prezzo di vendita : " + str(sell_price))
                st.write("IMEI : " + str(imei_code))
                st.write("Stato batteria : " + str(battery_health))
                st.write("Grado : " + grade)
                st.write("Capacità : " + str(capacity))
                st.write("Stato : " + status)


                st.subheader("Informazioni Cliente")
                st.write("Nome : " + customer_name)
                st.write("Cognome : " + customer_last_name)


                st.subheader("Altre informazioni")
                st.write("Venduto : " + sold)
                st.write("Data vendita : " + selling_date)
                st.write("Articolo : " + article_type)


            if i == 1 :
                break
           
    except Exception as e:
        #raise
        st.info("Scegli la riparazione da consultare" + str(e)) 







with col_2:
    with st.expander("Statistiche magazzino",expanded=True) : 


        # Handling missing values
        insights_df.fillna(method='ffill', inplace=True)  # Example: Forward-fill missing values
        # Converting dates to datetime format
        insights_df['selling_date'] = pd.to_datetime(insights_df['selling_date'])
        # Creating new columns if needed
        insights_df['sell_price'] = insights_df['sell_price'].astype(float)
        insights_df['price'] = insights_df['price'].astype(float)

        # Calcola il 'Margine_profitto' come la differenza tra 'sell_price' e 'price'
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
        st.pyplot(plt)        # Conta il numero di dispositivi per ogni stato
        n_dispositivi_per_stato = insights_df["status"].value_counts()
        plt.figure(figsize=(8, 6))
        n_dispositivi_per_stato.plot(kind="bar")
        plt.title("Distribuzione degli stati dei dispositivi")
        plt.xlabel("Stato")
        plt.ylabel("Numero di dispositivi")
        st.pyplot(plt)        # Conta il numero di dispositivi per ogni stato
        # Conta il numero di dispositivi per ogni brand
        n_dispositivi_per_brand = insights_df["brand"].value_counts()

        # Ordina i brand in base al numero di dispositivi
        n_dispositivi_per_brand = n_dispositivi_per_brand.sort_values(ascending=False)

        # Seleziona i primi 10 brand
        top_10_brand = n_dispositivi_per_brand.head(10)

        # Crea un grafico a barre per visualizzare i primi 10 brand con il maggior numero di dispositivi
        plt.figure(figsize=(12, 6))
        top_10_brand.plot(kind="bar")
        plt.title("Top 10 brand con il maggior numero di dispositivi")
        plt.xlabel("Brand")
        plt.ylabel("Numero di dispositivi")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        st.pyplot(plt)        # Conta il numero di dispositivi per ogni stato
        # ## Analisi del grado del dispositivo

        # Conta il numero di dispositivi per ogni grado
        n_dispositivi_per_grado = insights_df["grade"].value_counts()

        # Crea un grafico a torta per visualizzare la distribuzione dei gradi dei dispositivi
        plt.figure(figsize=(8, 6))
        n_dispositivi_per_grado.plot(kind="pie", autopct="%1.1f%%")
        plt.title("Distribuzione dei gradi dei dispositivi")
        st.pyplot(plt)        # Conta il numero di dispositivi per ogni stato


        if 'status' in insights_df.columns:
            # Creazione del grafico a torta
            fig, ax = plt.subplots()
            insights_df['status'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax)
            ax.set_ylabel('')  # Rimuove l'etichetta dell'asse y
            ax.set_title('Distribuzione dei Tipi di Dispositivo')
            # Mostra il grafico in Streamlit
            st.pyplot(fig)
        else:
            st.error('La colonna "status" non è presente nel DataFrame. Verifica i dati.')




    with st.expander("Inserisci dispositivo") :

        input_data = {
            'device_type': st.selectbox("Tipo dispositivo", options=["TV", "PC", "Smartphone", "Tablet"]), 
            'price': st.number_input("Prezzo", min_value=0.0, format="%.2f"),
            'sell_price': st.number_input("Prezzo di vendita", min_value=0.0, format="%.2f"), 
            'imei_code': st.text_input("imei_code"), 
            'battery_health': float, 
            'brand': st.text_input("Marca"), 
            'model': st.text_input("Modello"), 
            'grade': st.selectbox("Grado", options=["A", "B", "C", "D", "Premium"]), 
            'capacity': st.text_input("capacity"), 
            'status': st.selectbox("Stato", options=["Nuovo", "Usato", "Ricondizionato"]), 
            'manufacturer': st.text_input("manufacturer"), 
            'sold': str(st.checkbox("Venduto")), 
            'customer_name': st.text_input("customer_name"), 
            'customer_last_name': st.text_input("customer_last_name"), 
            'selling_date':  st.text_input("selling_date"), 
            'article_type':  st.text_input("article_type"),
        }

        # Bottoni per operazioni
        if st.button('Aggiungi'):
            try:
                # Convalida i dati usando il modello Pydantic
                reparation = Device(**input_data)
                add_device(inventory_worksheet, list(reparation.model_dump().values()))
                st.success("Reparation aggiunta con successo!")
            except Exception as e:
                st.error(f"Errore nella convalida dei dati: {str(e)}")


    with st.expander("Elimina dispositivo/i"):
        selected_index = st.selectbox("Seleziona l'ID della riga da rimuovere", range(len(insights_df)))
        if st.button('Rimuovi Reparation'):
            remove_device(inventory_worksheet, selected_index + 1)  # +1 perché l'indice del DataFrame parte da 0
            st.success(f"Reparation rimossa con successo dalla riga {selected_index + 1}")
            display_devices()  # Aggiorna la visualizzazione dei dati

    with st.expander("Modifica scheda dispositivo"):
        # Funzione per ottenere i dati
        def get_data():
            data = inventory_worksheet.get_all_records()
            return pd.DataFrame(data)

        # Visualizzazione dei dati con filtri
        df = get_data()
        filtro_stato = st.selectbox("Filtra per stato", ['Tutti'] + list(df['status'].unique()))
        if filtro_stato != 'Tutti':
            df = df[df['status'] == filtro_stato]

        st.write(df)

        selected_row_index = st.selectbox("Seleziona la riga da modificare:", df.index)
        selected_row = df.iloc[selected_row_index]

        # Form di modifica con valori predefiniti
        with st.form("edit_form"):
            new_data = {
                'request_date': st.text_input("Data"),
                'first_name': st.text_input("Nome"),
                'last_name': st.text_input("Cognome"),
                'phone_number': st.text_input("Numero di telefono"),
                'device': st.selectbox("Tipo dispositivo", options=["TV", "PC", "Smartphone", "Tablet"]),
                'brand': st.text_input("Marca"),
                'model': st.text_input("Modello"),
                'price': st.text_input("Prezzo"),
                'state': st.selectbox("Stato", options=["Consegnato", "In attesa", "Chiamato", "Annullato", "In sospeso"]),
                'operator': st.text_input("Operatore"),
                'left_accessory': st.checkbox("Accessori lasciati"),
                'unlock_code': st.text_input("Codice sblocco"),
                'color': st.text_input("Colore"),
                'action': st.text_input("Azione"),
                'url': st.text_input("Link"),
                'muletto': st.text_input("Muletto")
                #'data': st.text_input("Data", value=selected_row['data']),
                #'descrizione': st.text_input("Descrizione", value=selected_row['descrizione']),
                #'costo': st.number_input("Costo", value=float(selected_row['costo']), format="%.2f"),
                #'stato': st.selectbox("Stato", ['nuovo', 'usato', 'ricondizionato'], index=['nuovo', 'usato', 'ricondizionato'].index(selected_row['stato']))
            }

            submit_button = st.form_submit_button("Salva Modifiche")
            if submit_button:
                # Convalida i dati con il modello Pydantic
                try:
                    valid_data = Device(**new_data)
                    # Aggiorna i dati nella riga selezionata
                    inventory_worksheet.update(f'A{selected_row_index + 2}:D{selected_row_index + 2}', [list(valid_data.dict().values())])
                    st.success("Modifiche salvate con successo!")
                except Exception as e:
                    st.error(f"Errore di validazione: {str(e)}")

                # Ricarica i dati e aggiorna la visualizzazione
                df = get_data()  # Ricarica i dati
                st.write(df)     # Aggiorna la visualizzazione





st.sidebar.markdown('Spazio Exe - Inventory MGMT')
st.sidebar.markdown('<small>[Help Center](https://www.osirisolutions.com/helpcenter/spazioexe)</small>', unsafe_allow_html=True)
st.sidebar.markdown('<small>[Contact Us](mailto:paolo@osirisolutions.com)</small>', unsafe_allow_html=True)
st.sidebar.markdown('''<small>[Spazio Exe - Inventory Management v0.1](https://github.com/PaoloGouba/spazioexe_inventory_management)  | April 2024 | [Osiris Solutions](https://osirisolutions.com/)</small>''', unsafe_allow_html=True)
