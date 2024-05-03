import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import json

def auth_gspread():
    # Crea una stringa JSON dalle credenziali salvate come segreti
    creds_json = json.dumps({
        "type": st.secrets["google_creds"]["type"],
        "project_id": st.secrets["google_creds"]["project_id"],
        "private_key_id": st.secrets["google_creds"]["private_key_id"],
        "private_key": st.secrets["google_creds"]["private_key"],
        "client_email": st.secrets["google_creds"]["client_email"],
        "client_id": st.secrets["google_creds"]["client_id"],
        "auth_uri": st.secrets["google_creds"]["auth_uri"],
        "token_uri": st.secrets["google_creds"]["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["google_creds"]["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["google_creds"]["client_x509_cert_url"]
    })

    credentials = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(creds_json))
    try:
        gc = gspread.authorize(credentials)
        return gc
    except Exception as e:
        raise SystemExit(f"Errore nella chiamata a Google Sheet API: {e}")

def get_worksheet(worksheet_name):
    gc = auth_gspread()
    sh = gc.open(worksheet_name)
    worksheet = sh.sheet1
    return worksheet
