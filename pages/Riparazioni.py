import streamlit as st
from streamlit_extras.row import row
from streamlit_extras.app_logo import add_logo
from streamlit_extras.card import card
from modules.reparations import *
from modules.models import Reparation
from utils.tools import get_data, gen_recap
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = fetch_reparations(reparations_worksheet)

st.set_page_config(
    page_icon="🧊",
    page_title="Spazio Exé - Riparazioni", 
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        "Get Help" : "https://www.osirisolutions.com/helpcenter/spazioexe/riparazioni",
        "Report a bug" : "mailto:support@osirisolutions.com" #to improve with perso object or something to automate support
    }
)


add_logo("img/logo.webp")


from streamlit_modal import Modal

import streamlit.components.v1 as components


modal = Modal(
    "Demo Modal", 
    key="demo-modal",
    
    # Optional
    padding=20,    # default value
    max_width=744  # default value
)
#open_modal = st.button("Open")
#if open_modal:
#    modal.open()

#if modal.is_open():
#    with modal.container():
#        st.write("Text goes here")

#        html_string = '''
#        <h1>HTML string in RED</h1>

#        <script language="javascript">
#          document.querySelector("h1").style.color = "red";
#        </script>
#       '''
#        components.html(html_string)

#        st.write("Some fancy text")
#        value = st.checkbox("Check me")
#        st.write(f"Checkbox checked: {value}")

st.header('Riparazioni')

col_1, col_2 = st.columns(2)

with col_2: 

    with st.expander("Statistiche riparazioni", expanded=True) :

        insight_type = ("brand","")

        ## INSIGHTS RIPARAZIONI

        if 'price' in df.columns and 'brand' in df.columns and 'state' in df.columns and not df.empty:
            st.subheader("Totale riparazioni : "+ str(len(df)), divider=True)
            #average_price = df['price'].mean().round(2)
            #average_price_str = f"€{average_price:,.2f}"
            #print("Average Price of Devices:", average_price_str)

            orders_by_state = df['state'].value_counts()
            st.subheader("Riparazioni per stato:")
            # Grafico a barre per la distribuzione degli ordini per stato
            plt.figure(figsize=(10, 6))
            sns.barplot(x=orders_by_state.index, y=orders_by_state.values)
            plt.xlabel('Stato')
            plt.ylabel('Numero Ordini')
            plt.title('Distribuzione degli ordini per stato')
            plt.xticks(rotation=45)
            st.pyplot(plt)  # Usa st.pyplot() invece di plt.show()
            for state, count in orders_by_state.items():
                st.write(f" - {state}: {count} items")



            popular_brands = df['brand'].value_counts().head(5)
            st.subheader("I 5 Brand più riparati:")
            # Grafico a torta per i marchi più popolari
            plt.figure(figsize=(8, 8))
            plt.pie(popular_brands.values, labels=popular_brands.index, autopct='%1.1f%%')
            plt.title('Top 5 Popular Brands')
            st.pyplot(plt)  # Usa st.pyplot() invece di plt.show()
            i=1
            for brand, count in popular_brands.items():
                st.write(f"{str(i)}. {brand}: {count} items")
                i+=1



            



        ## OLD TEST INSIGHT
        #st.subheader("Deprecated")


        # Controllo delle colonne necessarie
        #if 'device' in df.columns and 'state' in df.columns:
            # Selezione dello stato da filtrare
        #    unique_status = df['state'].unique()
        #    selected_status = st.multiselect('Seleziona Stato/i', unique_status, default=unique_status)

            # Filtraggio dei dati basato sullo stato selezionato
        #    insight_filtered_df = df[df['state'].isin(selected_status)]

            # Creazione dell'istogramma
        #    fig, ax = plt.subplots()
        #    insight_filtered_df['device'].value_counts().plot(kind='bar', ax=ax, color='skyblue')
        #    ax.set_xlabel('Tipo di Dispositivo')
        #    ax.set_ylabel('Frequenza')
        #    ax.set_title('Distribuzione dei Tipi di Dispositivo per Stato Selezionato')
        #    plt.xticks(rotation=45)  # Ruota le etichette degli assi x per una migliore leggibilità

            # Mostra il grafico in Streamlit
        #    st.pyplot(fig)
        #else:
        #    st.error('Il DataFrame non contiene le colonne "device" o "status". Verifica i dati.')






    with st.expander("Nuova riparazione") :
        st.caption("Riparazione #C00001")
        input_data = {
            'first_name': st.text_input("Nome"),
            'last_name': st.text_input("Cognome"),
            'phone_number': st.text_input("Numero di telefono"),
            'device': st.selectbox("Tipo dispositivo", options=["TV", "PC", "Smartphone", "Tablet"]),
            'brand': st.text_input("Marca"),
            'model': st.text_input("Modello"),
            'price': st.text_input("Prezzo"),
            'state': st.selectbox("Stato", options=["Consegnato", "In attesa", "Chiamato", "Annullato", "In sospeso"]),
            'operator': st.text_input("Operatore"),
            'unlock_code': st.text_input("Codice sblocco"),
            'color': st.text_input("Colore"),
            'action': st.text_input("Azione"),
            'url': st.text_input("Link"),
            'muletto': st.checkbox("Muletto"),
            'left_accessory': st.checkbox("Accessori lasciati")
        }

        if st.button('Aggiungi riparazione'):
            try:
                reparation = Reparation(**input_data)
                add_reparation(reparations_worksheet, list(reparation.model_dump().values()))
                # generazione documento 
                temp_file_name="Reparation_"+input_data["first_name"]+".pdf"  
                file_download_name = gen_recap(input_data,temp_file_name)
                st.success("Reparation aggiunta con successo!")
            except Exception as e:
                #raise
                st.error(f"Errore nella convalida dei dati: {str(e)}")
     

    with st.expander("Modifica riparazione") :

        # Visualizzazione dei dati con filtri
        df = get_data(reparations_worksheet)
        filtro_stato = st.selectbox("Filtra per stato", ['Tutti'] + list(df['state'].unique()))
        if filtro_stato != 'Tutti':
            df = df[df['state'] == filtro_stato]

        st.write(df)

        selected_row_index = st.selectbox("Seleziona la riga da modificare:", df.index)
        selected_row = df.iloc[selected_row_index]

        # Form di modifica con valori predefiniti
        with st.form("edit_form"):
            # Input fields per i dati
            new_data = {
                'first_name': st.text_input("Nome"),
                'last_name': st.text_input("Cognome"),
                'phone_number': st.text_input("Numero di telefono"),
                'device': st.selectbox("Tipo dispositivo", options=["TV", "PC", "Smartphone", "Tablet"]),
                'brand': st.text_input("Marca"),
                'model': st.text_input("Modello"),
                'price': st.text_input("Prezzo"),
                'state': st.selectbox("Stato", options=["Consegnato", "In attesa", "Chiamato", "Annullato", "In sospeso"]),
                'operator': st.text_input("Operatore"),
                'unlock_code': st.text_input("Codice sblocco"),
                'color': st.text_input("Colore"),
                'action': st.text_input("Azione"),
                'url': st.text_input("Link"),
                'muletto': st.checkbox("Muletto"),
                'left_accessory': st.checkbox("Accessori lasciati")
            }

            submit_button = st.form_submit_button("Salva Modifiche")
            if submit_button:
                # Convalida i dati con il modello Pydantic
                try:
                    valid_data = Reparation(**new_data)
                    # Aggiorna i dati nella riga selezionata
                    reparations_worksheet.update(f'A{selected_row_index + 2}:D{selected_row_index + 2}', [list(valid_data.dict().values())])
                    st.success("Modifiche salvate con successo!")
                except Exception as e:
                    st.error(f"Errore di validazione: {str(e)}")

                # Ricarica i dati e aggiorna la visualizzazione
                df = get_data(reparations_worksheet)  # Ricarica i dati
                st.write(df)     # Aggiorna la visualizzazione


    #with st.expander("Elimina riparazione"):
        #selected_index = st.selectbox("Seleziona l'ID della riga da rimuovere", range(len(df)))
        #if st.button('Rimuovi Reparation'):
            #remove_reparation(reparations_worksheet, selected_index + 1)  # +1 perché l'indice del DataFrame parte da 0
            #st.success(f"Reparation rimossa con successo dalla riga {selected_index + 1}")
            #display_reparations()  # Aggiorna la visualizzazione dei dati




with col_1:
    with st.expander(label="Visualizza riparazioni") :
        
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
        # Mostra il DataFrame filtrato
        st.dataframe(filtered_df)
    try :
        i = 0
        for row in filtered_df.itertuples():
            i=i+1
            request_date = row.request_date
            first_name = row.first_name
            last_name = row.last_name
            phone_number = row.phone_number
            device = row.device
            brand = row.brand
            model = row.model
            price = row.price
            state = row.state
            operator = row.operator
            left_accessory = row.left_accessory
            unlock_code = row.unlock_code
            color = row.color
            action = row.action
            url = row.url
            muletto = row.muletto

            c_text : str = "Cliente : " + first_name + " " + last_name + "\n" + "Azione : " + action

            card(
                title=device + " - " + brand + " - " + state,
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
                "request_date" : request_date,
                "first_name" : first_name,
                "last_name" : last_name,
                "phone_number" : phone_number,
                "device" : device,
                "brand" : brand,
                "model" : model,
                "price" : price,
                "state" : state,
                "operator" : operator,
                "left_accessory" : left_accessory,
                "unlock_code" : unlock_code,
                "color" : color,
                "action" : action,
                "url" : url,
                "muletto" : muletto
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
                st.caption("Ref #76989JIBI")
                st.write("Data Richiesta : " + request_date)
                st.subheader("Informazioni Cliente")
                st.write("Nome : " + first_name)
                st.write("Cognome : " + last_name)
                st.write("Telefono : " + str(phone_number))
                st.subheader(f"Azione : {action}")
                st.subheader("Informazioni Dispositivo")
                st.write("Dispositivo : " + device)
                st.write(f"Marca : {brand}")
                st.write(f"Modello : {model}")
                st.write(f"Prezzo : {price}")
                st.write(f"Condizione : {state}")
                st.write(f"Colore : {color}")
                st.subheader("Altre informazioni")
                st.write(f"Operatore : {operator}")
                st.write(f"Accessorio lasciato : {left_accessory}")
                st.write(f"Codice sblocco : {unlock_code}")
                st.write(f"URL : {url}")
                st.write(f"Muletto : {muletto}")
            if i == 1 :
                break
           
    except Exception as e:
        #raise
        st.info("Scegli la riparazione da consultare" + str(e)) 






## Footer

st.sidebar.markdown('<small>[Help Center](https://www.osirisolutions.com/helpcenter/spazioexe)</small>', unsafe_allow_html=True)
st.sidebar.markdown('<small>[Contact Us](mailto:paolo@osirisolutions.com)</small>', unsafe_allow_html=True)
st.sidebar.markdown('''<small>[Spazio Exé - Inventory Management v0.1](https://github.com/PaoloGouba/spazioexe_inventory_management)  | April 2024 | [Osiris Solutions](https://osirisolutions.com/)</small>''', unsafe_allow_html=True)





