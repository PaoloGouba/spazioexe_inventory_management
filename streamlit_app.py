import streamlit as st
from streamlit_extras.card import card

st.set_page_config(
    page_icon="🧊",
    page_title="Spazio Exé", 
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help" : "https://www.osirisolutions.com/helpcenter/spazioexe",
        "Report a bug" : "mailto:support@osirisolutions.com"
    }
)

st.sidebar.markdown('Spazio Exé - Inventory MGMT')
st.sidebar.markdown('<small>[Help Center](https://www.osirisolutions.com/helpcenter/spazioexe)</small>', unsafe_allow_html=True)
st.sidebar.markdown('<small>[Contact Us](mailto:paolo@osirisolutions.com)</small>', unsafe_allow_html=True)
st.sidebar.markdown('''<small>[Spazio Exé - Inventory Management v0.1](https://github.com/PaoloGouba/spazioexe_inventory_management)  | April 2024 | [Osiris Solutions](https://osirisolutions.com/)</small>''', unsafe_allow_html=True)



#st.markdown("<h1 style='text-align: center; color: black;'>Spazio Exé - Inventory</h1><h1 style='text-align: center; color: orange;'>MGMT</h1>", unsafe_allow_html=True)
st.title("Spazio Exé - Inventory MGMT")
col_1, col_2 = st.columns(2)

with col_1:
    card(
        title="Dashboard",
        text="Una vista generale suoi tuoi dati",
        url="https://www.google.com",
    )
    card(
        title="Magazzino",
        text="Gestisci il magazzino Spazio Exé",
        image="http://placekitten.com/300/250",
        url="http://localhost:8501/Dispositivi",
    )

with col_2:
    card(
        title="Centro Riparazioni",
        text="Gestisci le riparazioni Spazio Exé",
        image="http://placekitten.com/300/250",
        url="http://localhost:8501/Riparazioni",
    )
    card(
        title="Registro cassa",
        text="Some description",
        image="http://placekitten.com/300/250",
        url="http://localhost:8501/Registro_cassa",
    )


       


