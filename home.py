import streamlit as st
from streamlit_extras.card import card
from streamlit_extras.app_logo import add_logo
st.set_page_config(
    page_icon="🧊",
    page_title="Spazio Exe", 
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help" : "https://www.osirisolutions.com/helpcenter/spazioexe",
        "Report a bug" : "mailto:support@osirisolutions.com"
    }
)
add_logo("img/logo.webp")

st.sidebar.markdown('Spazio Exe - Inventory MGMT')
st.sidebar.markdown('<small>[Help Center](https://www.osirisolutions.com/helpcenter/spazioexe)</small>', unsafe_allow_html=True)
st.sidebar.markdown('<small>[Contact Us](mailto:paolo@osirisolutions.com)</small>', unsafe_allow_html=True)
st.sidebar.markdown('''<small>[Spazio Exe - Inventory Management v0.1](https://github.com/PaoloGouba/spazioexe_inventory_management)  | April 2024 | [Osiris Solutions](https://osirisolutions.com/)</small>''', unsafe_allow_html=True)



#st.markdown("<h1 style='text-align: center; color: black;'>Spazio Exe - Inventory</h1><h1 style='text-align: center; color: orange;'>MGMT</h1>", unsafe_allow_html=True)
st.title("Spazio Exe - Inventory MGMT")
col_1, col_2 = st.columns(2)

with col_1:
    card(
        title="Dashboard",
        text="Una vista generale suoi tuoi dati",
        url="#",
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
    card(
        title="Magazzino",
        text="Gestisci il magazzino Spazio Exe",
        image="#",
        url="https://test-spazioexe-inventory.streamlit.app/Magazzino",
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

with col_2:
    card(
        title="Centro Riparazioni",
        text="Gestisci le riparazioni Spazio Exe",
        url="https://test-spazioexe-inventory.streamlit.app/Riparazioni",
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
    card(
        title="Registro cassa",
        text="Some description",
        url="#",                
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


       


