from gspread import *
import pandas as pd
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials

from utils.api_handler import auth_gspread,get_worksheet
from utils.tools import REP_FILE_NAME

reparations_worksheet = get_worksheet(REP_FILE_NAME)

def add_reparation(worksheet : Worksheet, reparation_data):
    worksheet.append_row(reparation_data)

def remove_reparation(worksheet : Worksheet, row_id):
    """ Rimuove una riga dal worksheet basandosi sull'ID della riga fornito. """
    # Gspread conta le righe a partire da 1
    worksheet.delete_rows(row_id + 1)

def update_reparation(worksheet : Worksheet, row_id, reparation_data):
    worksheet.update('A{}:Z{}'.format(row_id, row_id), [reparation_data])

def fetch_reparations(worksheet : Worksheet):
    data = worksheet.get_all_records()
    return pd.DataFrame(data)

def display_reparations():
    df = fetch_reparations(reparations_worksheet)
    st.dataframe(df)
    return df
