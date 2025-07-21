import streamlit as st
import pandas as pd
gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

# Paramètres
SHEET_ID = "1dqAx5719sRx_J1Ce34Of0eIXCk275wyLcJcIusIRMwg"
SHEET_NAME = "Sheet1"

# Authentification Google Sheets (lecture seule)
creds_json = os.environ.get("GOOGLE_SHEETS_CREDS")
if not creds_json:
    st.error("La variable d'environnement GOOGLE_SHEETS_CREDS n'est pas définie.")
    st.stop()
creds_dict = json.loads(creds_json)

scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
gc = gspread.authorize(creds)

# Lire les données du Google Sheet
def get_data():
    sh = gc.open_by_key(SHEET_ID)
    worksheet = sh.worksheet(SHEET_NAME)
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
    if not df.empty:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
    return df

df = get_data()

st.title("Historique des points Hybra")

if df.empty:
    st.info("Aucune donnée disponible.")
else:
    st.subheader("Tableau des points et rangs")
    st.dataframe(df)

    st.subheader("Évolution des points et du rang")
    col1, col2 = st.columns(2)
    with col1:
        st.line_chart(df.set_index('timestamp')['totalPoints'], height=300)
    with col2:
        st.line_chart(df.set_index('timestamp')['rank'], height=300) 