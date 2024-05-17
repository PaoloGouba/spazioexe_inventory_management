import gspread
import pandas as pd
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials


from utils.api_handler import auth_gspread,get_worksheet
from utils.tools import DEVICES_FILE_NAME

inventory_worksheet = get_worksheet(DEVICES_FILE_NAME)



def add_device(worksheet, device_data):
    worksheet.append_row(device_data)


def remove_device(worksheet, row_id):
    """ Rimuove una riga dal worksheet basandosi sull'ID della riga fornito. """
    # Gspread conta le righe a partire da 1
    worksheet.delete_rows(row_id + 1)



def update_device(worksheet, row_id, device_data):
    worksheet.update('A{}:Z{}'.format(row_id, row_id), [device_data])


def fetch_device(worksheet):
    data = worksheet.get_all_records()
    return pd.DataFrame(data)



def display_devices():
    df = fetch_device(inventory_worksheet)
    st.write(df)
    return df
